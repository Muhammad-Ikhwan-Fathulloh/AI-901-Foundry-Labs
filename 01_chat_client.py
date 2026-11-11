"""
Modul 01: Chat Client Interaktif dengan Azure AI Foundry & OpenAI SDK.

Deskripsi:
Aplikasi percakapan interaktif berbasis antarmuka baris perintah (CLI).
Mengimplementasikan context history percakapan secara multi-turn dengan LLM
yang di-deploy di Azure AI Foundry.

Cara Menjalankan:
    python 01_chat_client.py
    (Ketik "exit" atau "keluar" untuk berhenti)
"""
from common import env, openai_client

SYSTEM_PROMPT = (
    "Anda adalah asisten layanan pelanggan toko online terpercaya. "
    "Jawab dengan ramah, jelas, dan singkat dalam bahasa Indonesia. "
    "Fokus pada penyelesaian masalah pelanggan dan jangan membahas harga pesaing."
)


def main():
    print("=" * 60)
    print("Modul 01: Chat Client Interaktif (AI-901)")
    print("=" * 60)

    client = openai_client()
    deployment = env("AZURE_AI_CHAT_DEPLOYMENT")
    history = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("Koneksi berhasil. Ketik 'exit' atau 'keluar' untuk mengakhiri chat.\n")
    while True:
        try:
            user_text = input("Anda   : ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nSesi chat dihentikan.")
            break

        if not user_text:
            continue
        if user_text.lower() in ("exit", "keluar", "quit", "q"):
            print("Terima kasih telah menggunakan layanan ini. Sampai jumpa!")
            break

        history.append({"role": "user", "content": user_text})

        try:
            response = client.chat.completions.create(
                model=deployment,
                messages=history,
                temperature=0.3,
                max_tokens=300,
            )
            answer = response.choices[0].message.content
            history.append({"role": "assistant", "content": answer})
            print(f"Asisten: {answer}\n")
        except Exception as e:
            print(f"[ERROR] Gagal memanggil model: {e}\n")


if __name__ == "__main__":
    main()
