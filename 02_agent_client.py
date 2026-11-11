"""
Modul 02: Azure AI Agent Service Client.

Deskripsi:
Memanggil agen AI yang telah dibuat dan dikonfigurasi melalui Azure AI Foundry.
Agen ini memiliki kemampuan grounding, instruksi spesifik, serta kemampuan
memanfaatkan knowledge base atau custom tools.

Cara Menjalankan:
    python 02_agent_client.py
"""
from common import env, openai_client


def main():
    print("=" * 60)
    print("Modul 02: Azure AI Agent Service Client (AI-901)")
    print("=" * 60)

    client = openai_client()
    agent_name = env("AZURE_AI_AGENT_NAME")

    questions = [
        "Apa saja syarat pendaftaran program beasiswa?",
        "Apakah ada jaminan kelulusan bagi pendaftar?",
        "Kapan batas akhir pendaftaran gelombang 1?",
    ]

    print(f"Memanggil Agen: '{agent_name}'\n")

    for idx, q in enumerate(questions, start=1):
        print(f"[{idx}] Pertanyaan: {q}")
        try:
            response = client.responses.create(
                input=[{"role": "user", "content": q}],
                extra_body={"agent": {"name": agent_name, "type": "agent_reference"}},
            )
            answer = getattr(response, "output_text", None) or str(response)
            print(f"    Jawaban   : {answer}\n")
        except Exception as e:
            print(f"    [ERROR] Gagal menghubungi agen: {e}\n")


if __name__ == "__main__":
    main()
