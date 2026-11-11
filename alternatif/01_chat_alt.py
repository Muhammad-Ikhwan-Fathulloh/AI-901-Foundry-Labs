"""
Alternatif 01: Chat Client Interaktif dengan Model AI Non-Azure.
Mendukung: Ollama (Lokal), OpenAI Langsung, atau Google Gemini.

Cara Menjalankan:
    python alternatif/01_chat_alt.py
"""
import sys
import os

# Tambahkan direktori saat ini ke path import
sys.path.append(os.path.dirname(__file__))

from config_alt import get_alternative_client, get_model_name, get_provider

SYSTEM_PROMPT = (
    "Anda adalah asisten layanan pelanggan toko online terpercaya. "
    "Jawab dengan ramah, jelas, dan singkat dalam bahasa Indonesia. "
    "Fokus pada penyelesaian masalah pelanggan dan jangan membahas harga pesaing."
)


def main():
    provider = get_provider()
    model = get_model_name("chat")

    print("=" * 60)
    print("Modul Alternatif 01: Chat Client Interaktif")
    print(f"Provider Terpilih : {provider.upper()}")
    print(f"Model Digunakan   : {model}")
    print("=" * 60)

    try:
        client = get_alternative_client()
    except Exception as e:
        print(f"[ERROR] Inisialisasi klien gagal: {e}")
        return

    history = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("Koneksi siap! Ketik 'exit' atau 'keluar' untuk mengakhiri chat.\n")
    while True:
        try:
            user_text = input("Anda   : ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nSesi chat dihentikan.")
            break

        if not user_text:
            continue
        if user_text.lower() in ("exit", "keluar", "quit", "q"):
            print("Sampai jumpa!")
            break

        history.append({"role": "user", "content": user_text})

        try:
            response = client.chat.completions.create(
                model=model,
                messages=history,
                temperature=0.3,
                max_tokens=300,
            )
            answer = response.choices[0].message.content
            history.append({"role": "assistant", "content": answer})
            print(f"Asisten: {answer}\n")
        except Exception as e:
            print(f"[ERROR] Gagal mendapatkan respon dari {provider}: {e}")
            if provider == "ollama":
                print("Tips: Pastikan aplikasi Ollama sedang berjalan ('ollama serve') dan model sudah ditarik ('ollama pull llama3.2').\n")


if __name__ == "__main__":
    main()
