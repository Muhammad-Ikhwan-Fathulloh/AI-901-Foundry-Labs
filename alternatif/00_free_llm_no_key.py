"""
Modul 00: LLM 100% Gratis Tanpa API Key (Open Source Lokal / In-Memory).

Deskripsi:
Modul ini menjalankan model bahasa (LLM) langsung di komputer/laptop Anda
menggunakan library Hugging Face Transformers.
- TIDAK MEMERLUKAN akun / pendaftaran apapun.
- TIDAK MEMERLUKAN API Key (OpenAI, Azure, maupun Gemini).
- TIDAK MEMERLUKAN kartu kredit atau kuota token berbayar.
- Berjalan langsung di CPU atau GPU lokal (sangat cocok juga untuk Google Colab gratis).

Model default yang digunakan: 'Qwen/Qwen2.5-0.5B-Instruct' atau 'HuggingFaceTB/SmolLM2-135M-Instruct'
(Sangat ringan, ukuran file kecil, cepat di laptop tanpa GPU diskrit).

Cara Menjalankan:
    python alternatif/00_free_llm_no_key.py
"""
import sys
import os

def check_dependencies():
    try:
        import torch
        import transformers
    except ImportError:
        print("[ERROR] Paket 'torch' dan 'transformers' diperlukan untuk menjalankan model tanpa API key.")
        print("Silakan pasang melalui perintah: pip install torch transformers")
        sys.exit(1)


def load_free_pipeline(model_id: str = "Qwen/Qwen2.5-0.5B-Instruct"):
    """
    Memuat model LLM open-source langsung ke memori (CPU/GPU) tanpa API Key.
    """
    import torch
    from transformers import pipeline

    print(f"\n[INFO] Memuat model open-source '{model_id}'...")
    print("[INFO] Jika ini pertama kali, bobot model akan diunduh sekali (sekitar 700 MB - 1 GB).")

    device = 0 if torch.cuda.is_available() else -1
    device_name = "GPU (CUDA)" if device == 0 else "CPU"
    print(f"[INFO] Perangkat eksekusi: {device_name}")

    pipe = pipeline(
        "text-generation",
        model=model_id,
        torch_dtype=torch.float32 if device == -1 else torch.float16,
        device=device
    )
    print("[OK] Model berhasil dimuat ke memori!\n")
    return pipe


def chat_tanpa_api_key(pipe):
    """Sesi tanya-jawab interaktif tanpa API Key."""
    print("=" * 65)
    print("Sesi Chat Bebas Biaya (100% Offline / Tanpa API Key)")
    print("Ketik 'exit' atau 'keluar' untuk mengakhiri.")
    print("=" * 65)

    system_prompt = (
        "Anda adalah asisten AI cerdas dan ramah. "
        "Jawab pertanyaan pengguna secara ringkas dan informatif dalam bahasa Indonesia."
    )

    while True:
        try:
            user_input = input("\nAnda: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nSesi chat dihentikan.")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "keluar", "quit", "q"):
            print("Sampai jumpa!")
            break

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_input}
        ]

        try:
            output = pipe(
                messages,
                max_new_tokens=256,
                temperature=0.3,
                do_sample=True,
                pad_token_id=pipe.tokenizer.eos_token_id
            )
            # Ambil respon pesan terakhir dari assistant
            response_text = output[0]["generated_text"][-1]["content"]
            print(f"\nAI (Lokal Bebas Key): {response_text.strip()}")
        except Exception as e:
            print(f"[ERROR Eksekusi]: {e}")


def demo_analisis_teks_tanpa_key(pipe):
    """Demo analisis sentimen ulasan tanpa API Key."""
    print("\n" + "=" * 65)
    print("Demo Ekstraksi & Analisis Teks Tanpa API Key")
    print("=" * 65)

    ulasan_sampel = "Barang sudah sampai tepat waktu dan kualitasnya sangat memuaskan!"
    prompt = (
        f"Analisis sentimen dari ulasan berikut: \"{ulasan_sampel}\". "
        f"Jawab dengan format:\nSentimen: [Positif/Negatif/Netral]\nAlasan: [Alasan singkat]"
    )

    messages = [
        {"role": "user", "content": prompt}
    ]

    print(f"Menganalisis: \"{ulasan_sampel}\"")
    output = pipe(messages, max_new_tokens=100, temperature=0.1)
    hasil = output[0]["generated_text"][-1]["content"]
    print(f"Hasil Analisis:\n{hasil.strip()}\n")


def main():
    print("=" * 65)
    print("Modul 00: LLM Bebas Biaya & Tanpa API Key (AI-901)")
    print("=" * 65)

    check_dependencies()

    # Model default yang efisien dan cerdas
    model_name = os.getenv("FREE_LOCAL_MODEL", "Qwen/Qwen2.5-0.5B-Instruct")
    
    try:
        pipe = load_free_pipeline(model_name)
    except Exception as e:
        print(f"[ERROR Gagal Memuat Model]: {e}")
        print("Alternatif: Anda juga dapat menggunakan Ollama secara lokal ('ollama run llama3.2')")
        return

    # Demo 1: Analisis cepat
    demo_analisis_teks_tanpa_key(pipe)

    # Demo 2: Chat interaktif
    chat_tanpa_api_key(pipe)


if __name__ == "__main__":
    main()
