"""
P-L2.7: Speech synthesis (teks ke suara) dan speech recognition (suara ke teks)
memakai Azure Speech di Foundry Tools.

Alur:
1. Ubah teks pengumuman menjadi file WAV (synthesis).
2. Baca kembali file WAV tersebut menjadi teks (recognition).
3. Bandingkan hasilnya dengan teks asli.
"""
import os
import azure.cognitiveservices.speech as speechsdk
from common import env

TEXT = "Selamat datang di layanan pelanggan. Pesanan Anda sedang kami proses."
VOICE = "id-ID-ArdiNeural"
OUT_WAV = os.path.join("output", "pengumuman.wav")


def make_config():
    cfg = speechsdk.SpeechConfig(subscription=env("AZURE_SPEECH_KEY"), region=env("AZURE_SPEECH_REGION"))
    cfg.speech_recognition_language = "id-ID"
    return cfg


def synthesize(cfg):
    os.makedirs("output", exist_ok=True)
    cfg.speech_synthesis_voice_name = VOICE
    audio_out = speechsdk.audio.AudioOutputConfig(filename=OUT_WAV)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=cfg, audio_config=audio_out)
    result = synthesizer.speak_text_async(TEXT).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"Audio dibuat: {OUT_WAV}")
    else:
        raise SystemExit(f"Synthesis gagal: {result.reason}")


def recognize(cfg):
    audio_in = speechsdk.audio.AudioConfig(filename=OUT_WAV)
    recognizer = speechsdk.SpeechRecognizer(speech_config=cfg, audio_config=audio_in)
    result = recognizer.recognize_once_async().get()
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    raise SystemExit(f"Recognition gagal: {result.reason}")


def main():
    cfg = make_config()
    synthesize(cfg)
    transcript = recognize(cfg)
    print("Teks asli   :", TEXT)
    print("Hasil dengar:", transcript)


if __name__ == "__main__":
    main()
