"""
Alternatif 04: Layanan Suara 100% Gratis (Edge-TTS & Whisper).

Deskripsi:
- Text-to-Speech (TTS): Menggunakan library 'edge-tts' yang mengakses suara Neural Microsoft
  (id-ID-ArdiNeural / id-ID-GadisNeural) secara gratis tanpa memerlukan langganan Azure atau API Key.
- Speech-to-Text (STT): Menggunakan model OpenAI Whisper (lokal / open source) untuk transkripsi audio.

Cara Menjalankan:
    python alternatif/04_speech_free_alt.py
"""
import asyncio
import os
import sys

TEXT = "Selamat datang di layanan pelanggan toko online kami. Pesanan Anda sedang diproses oleh tim gudang."
VOICE = "id-ID-ArdiNeural"  # Alternatif: "id-ID-GadisNeural"
OUT_AUDIO = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output", "pengumuman_free.mp3")


async def run_edge_tts(text: str, voice: str, out_file: str):
    """Men-generate audio suara natural Microsoft secara gratis via edge-tts."""
    try:
        import edge_tts
    except ImportError:
        print("[ERROR] Library 'edge-tts' belum terpasang. Jalankan: pip install edge-tts")
        return False

    os.makedirs(os.path.dirname(out_file), exist_ok=True)
    print(f"1. Mengonversi teks ke suara (Edge-TTS - Suara: {voice})...")
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(out_file)
    print(f"   [OK] Audio berhasil dibuat: {out_file}")
    return True


def run_whisper_stt(audio_file: str) -> str:
    """Mentranskripsikan audio kembali menjadi teks menggunakan model Whisper lokal."""
    try:
        import whisper
    except ImportError:
        return "[INFO] Paket 'openai-whisper' belum dipasang atau dilewati. Jalankan: pip install openai-whisper"

    print("2. Mentranskripsi audio ke teks (Whisper Speech-to-Text)...")
    try:
        # Menggunakan model 'tiny' atau 'base' agar cepat dan ringan di komputer lokal
        model = whisper.load_model("tiny")
        result = model.transcribe(audio_file, language="id")
        return result.get("text", "").strip()
    except Exception as e:
        return f"[ERROR Whisper]: {e}"


def main():
    print("=" * 60)
    print("Modul Alternatif 04: Speech AI 100% Gratis (Edge-TTS & Whisper)")
    print("=" * 60)

    # Langkah 1: Text-to-Speech
    tts_success = asyncio.run(run_edge_tts(TEXT, VOICE, OUT_AUDIO))
    if not tts_success:
        return

    # Langkah 2: Speech-to-Text (Whisper)
    print("\nMelakukan pengenalan suara (Speech Recognition)...")
    transcript = run_whisper_stt(OUT_AUDIO)

    print("\n--- Evaluasi Akurasi ---")
    print(f"Teks Asli        : {TEXT}")
    print(f"Hasil Transkripsi: {transcript}")
    print("=" * 60)


if __name__ == "__main__":
    main()
