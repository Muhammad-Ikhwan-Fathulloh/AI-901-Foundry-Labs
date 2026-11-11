"""
Modul 04: Layanan Suara (Speech-to-Text & Text-to-Speech) dengan Azure AI Speech.

Deskripsi:
1. Speech Synthesis (Text-to-Speech / TTS): Mengonversi teks berbahasa Indonesia ke file suara WAV.
2. Speech Recognition (Speech-to-Text / STT): Mengenali dan mentranskripsi file WAV kembali menjadi teks.
3. Evaluasi: Memvalidasi teks asli dengan hasil transkripsi model speech.

Cara Menjalankan:
    python 04_speech.py
"""
import os
import azure.cognitiveservices.speech as speechsdk
from common import env

TEXT = "Selamat datang di layanan pelanggan. Pesanan Anda sedang kami proses."
VOICE = "id-ID-ArdiNeural"
OUT_WAV = os.path.join("output", "pengumuman.wav")


def make_config():
    key = env("AZURE_SPEECH_KEY")
    region = env("AZURE_SPEECH_REGION")
    cfg = speechsdk.SpeechConfig(subscription=key, region=region)
    cfg.speech_recognition_language = "id-ID"
    return cfg


def synthesize(cfg):
    os.makedirs("output", exist_ok=True)
    cfg.speech_synthesis_voice_name = VOICE
    audio_out = speechsdk.audio.AudioOutputConfig(filename=OUT_WAV)
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=cfg, audio_config=audio_out)

    print("1. Mengonversi teks ke audio WAV (Speech Synthesis)...")
    result = synthesizer.speak_text_async(TEXT).get()

    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print(f"   [OK] Audio berhasil dibuat: {OUT_WAV}")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        raise SystemExit(f"   [ERROR] Synthesis dibatalkan: {cancellation.reason}. Detail: {cancellation.error_details}")
    else:
        raise SystemExit(f"   [ERROR] Synthesis gagal: {result.reason}")


def recognize(cfg) -> str:
    print("2. Membaca kembali file WAV menjadi teks (Speech Recognition)...")
    audio_in = speechsdk.audio.AudioConfig(filename=OUT_WAV)
    recognizer = speechsdk.SpeechRecognizer(speech_config=cfg, audio_config=audio_in)
    result = recognizer.recognize_once_async().get()

    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        raise SystemExit("   [WARNING] Suara tidak terdeteksi atau tidak cocok dengan bahasa id-ID.")
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation = result.cancellation_details
        raise SystemExit(f"   [ERROR] Recognition dibatalkan: {cancellation.reason}. Detail: {cancellation.error_details}")
    raise SystemExit(f"   [ERROR] Recognition gagal: {result.reason}")


def main():
    print("=" * 60)
    print("Modul 04: Azure AI Speech Service (AI-901)")
    print("=" * 60)

    cfg = make_config()
    synthesize(cfg)
    transcript = recognize(cfg)

    print("\n--- Evaluasi Akurasi Transkripsi ---")
    print(f"Teks Asli        : {TEXT}")
    print(f"Hasil Transkripsi: {transcript}")
    print("Status           : Berhasil.")


if __name__ == "__main__":
    main()
