"""
P-L2.5: Client ringan yang memanggil agen yang sudah dibuat di portal (L2.4).
Nama agen diambil dari .env (AZURE_AI_AGENT_NAME).

[VERIFY] Nama method dan parameter agen bisa berbeda antar versi SDK.
Jika error, cek dokumentasi azure-ai-projects versi yang terpasang.
"""
from common import env, openai_client


def main():
    client = openai_client()
    agent_name = env("AZURE_AI_AGENT_NAME")

    questions = [
        "Apa saja syarat pendaftaran?",
        "Apakah saya dijamin dapat beasiswa?",
        "Kapan batas akhir pendaftaran gelombang 1?",
    ]

    for q in questions:
        response = client.responses.create(
            input=[{"role": "user", "content": q}],
            extra_body={"agent": {"name": agent_name, "type": "agent_reference"}},
        )
        print(f"Pertanyaan: {q}")
        print(f"Jawaban   : {response.output_text}\n")


if __name__ == "__main__":
    main()
