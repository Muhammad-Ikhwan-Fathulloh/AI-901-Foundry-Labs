"""
P-L2.3: Chat client sederhana dengan Foundry SDK.
Jalankan: python 01_chat_client.py
Ketik "exit" untuk berhenti.
"""
from common import env, openai_client

SYSTEM_PROMPT = (
    "Anda adalah asisten layanan pelanggan toko online fiktif. "
    "Jawab singkat dalam bahasa Indonesia. Jangan membahas harga pesaing."
)


def main():
    client = openai_client()
    deployment = env("AZURE_AI_CHAT_DEPLOYMENT")
    history = [{"role": "system", "content": SYSTEM_PROMPT}]

    print("Chat dimulai. Ketik 'exit' untuk keluar.")
    while True:
        user_text = input("Anda: ").strip()
        if user_text.lower() == "exit":
            break
        history.append({"role": "user", "content": user_text})

        response = client.chat.completions.create(
            model=deployment,
            messages=history,
            temperature=0.2,
            max_tokens=300,
        )
        answer = response.choices[0].message.content
        history.append({"role": "assistant", "content": answer})
        print(f"Asisten: {answer}\n")


if __name__ == "__main__":
    main()
