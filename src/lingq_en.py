import requests
import csv
import os
from os.path import join, dirname
from dotenv import load_dotenv
from google.cloud import texttospeech
from google.oauth2 import service_account

# 言語ごとの設定変数
LANGUAGE_CODE = "en"
TTS_LANGUAGE_CODE = "en-US"
TTS_NAME = "en-US-Wavenet-D"
TTS_SSML_GENDER = texttospeech.SsmlVoiceGender.MALE

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.environ.get("LingQ_API_KEY")
API_URL = f'https://www.lingq.com/api/v2/{LANGUAGE_CODE}/cards/'
API_HEADER = {'Authorization':f'token {TOKEN}'}

CREDENTIAL_PATH = os.environ.get("TTS_CREDENTIAL_PATH")
ANKI_AUDIO_DIR = os.environ.get("ANKI_AUDIO_DIR")

def tts(client, text, filename, voice, audio_config):    
    audio_path = join(ANKI_AUDIO_DIR, filename)
    if os.path.exists(audio_path):
        print(f"{filename} exists")
        return

    input_text = texttospeech.SynthesisInput(text=text)
    
    response = client.synthesize_speech(request={"input": input_text, "voice": voice, "audio_config": audio_config})

    with open(audio_path, 'wb') as out:
        out.write(response.audio_content)
        print(f'Audio content written to file {filename}')

def main():
    # TTS の設定
    credentials = service_account.Credentials.from_service_account_file(CREDENTIAL_PATH)
    client = texttospeech.TextToSpeechClient(credentials=credentials)
    voice = texttospeech.VoiceSelectionParams(
        language_code=TTS_LANGUAGE_CODE,
        name=TTS_NAME,
        ssml_gender=TTS_SSML_GENDER ,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    r = requests.get(API_URL, headers=API_HEADER).json()
    results = r["results"]

    words = []

    for result in results:
        word = result["hints"][0]
        text = ' '.join(result["words"])
        replaced_text = text.replace('.', '')
        filename = f'lingq_{LANGUAGE_CODE}_{replaced_text}.mp3'

        tts(client, text, filename, voice, audio_config)
        # 言語ごとの設定 id, term, japanese, phrase, audio
        words.append([word["id"], text, word["text"], result["fragment"], f"[sound:{filename}]"]) 

    with open(f'../csv/LingQ {LANGUAGE_CODE}.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(words)

if __name__ == '__main__':
    main()