"""
P-L2.6: Aplikasi analisis teks sederhana.
Membaca data/ulasan.txt (satu ulasan per baris), lalu menulis hasil JSON ke output/.
"""
import json
import os
from common import env, openai_client

PROMPT = """Analisis ulasan berikut. Balas HANYA dengan JSON valid dengan kunci:
- "keywords": daftar kata kunci (string)
- "entities": daftar objek {"text": ..., "type": "product|location|brand|person|other"}
- "sentiment": salah satu dari "positive", "negative", "neutral", "mixed"
- "summary": satu kalimat dalam bahasa Indonesia

Ulasan: \"\"\"{review}\"\"\""""


def analyze(client, deployment, review):
    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": PROMPT.format(review=review)}],
        temperature=0,
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)


def main():
    client = openai_client()
    deployment = env("AZURE_AI_CHAT_DEPLOYMENT")

    with open("data/ulasan.txt", encoding="utf-8") as f:
        reviews = [line.strip() for line in f if line.strip()]

    results = []
    for i, review in enumerate(reviews, start=1):
        try:
            data = analyze(client, deployment, review)
        except json.JSONDecodeError:
            data = {"error": "output bukan JSON valid"}
        results.append({"no": i, "ulasan": review, "hasil": data})
        print(f"[{i}] {data.get('sentiment', 'error')}: {data.get('summary', '')}")

    os.makedirs("output", exist_ok=True)
    with open("output/hasil_analisis.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print("\nHasil disimpan di output/hasil_analisis.json")


if __name__ == "__main__":
    main()
