import requests
import csv
import os
from os.path import join, dirname
from dotenv import load_dotenv
from google.cloud import texttospeech
from google.oauth2 import service_account

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.environ.get("LingQ_API_KEY")
API_URL = 'https://www.lingq.com/api/v2/en/cards/'
API_HEADER = {'Authorization':f'token {TOKEN}'}

CREDENTIAL_PATH = os.environ.get("TTS_CREDENTIAL_PATH")
AUDIO_DIR_NAME = os.environ.get("AUDIO_DIR_NAME_EN")
AUDIO_DIR_PATH = os.environ.get("AUDIO_DIR_PATH_EN")

def tts(client, text, filename, voice, audio_config):    
    audio_path = join(dirname(__file__), filename)
    if os.path.exists(audio_path):
        print(f"{filename} exists")
        return

    input_text = texttospeech.SynthesisInput(text=text)
    
    response = client.synthesize_speech(request={"input": input_text, "voice": voice, "audio_config": audio_config})

    with open(filename, 'wb') as out:
        out.write(response.audio_content)
        print(f'Audio content written to file {filename}')

def main():
    # TTS の設定
    credentials = service_account.Credentials.from_service_account_file(CREDENTIAL_PATH)
    client = texttospeech.TextToSpeechClient(credentials=credentials)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US",
        name="en-US-Wavenet-D",
        ssml_gender=texttospeech.SsmlVoiceGender.MALE,
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # text = "test"
    # tts(client, text, voice, audio_config)

    r = requests.get(API_URL, headers=API_HEADER).json()
    results = r["results"]

    words = []

    for result in results:
        word = result["hints"][0]
        text = ' '.join(result["words"])
        replaced_text = text.replace('.', '')
        filename = f'{AUDIO_DIR_NAME}/{replaced_text}.mp3'
        audio_path = f'{AUDIO_DIR_PATH}{replaced_text}.mp3'

        tts(client, text, filename, voice, audio_config)
        words.append([word["id"], text, word["text"], result["fragment"], f"[sound:{audio_path}]"]) # id, english, japanese, phrase, audio

    with open('LingQ en.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerows(words)

if __name__ == '__main__':
    main()