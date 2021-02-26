"""Google Text to Speech 用"""

from google.cloud import texttospeech
from google.oauth2 import service_account

class TTS:
    def __init__(self, cfg: Dict):
        _credentials = service_account.Credentials.from_service_account_file(cfg.credential_path)
        self.client = texttospeech.TextToSpeechClient(credentials=_credentials)
        self.voice = texttospeech.VoiceSelectionParams(
            language_code=cfg.language_code,
            name=cfg.name,
            ssml_gender=cfg.gender ,
        )
        self.audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.MP3
        )

    def synth(self, text):
        _input_text = texttospeech.SynthesisInput(text=text)
        _request = {"input": _input_text, "voice": self.voice, "audio_config": self.audio_config}
        response = self.client.synthesize_speech(request=_request)

        return response