"""
Modul 03: Analisis Teks Berstruktur (Sentimen, Entitas, Ringkasan).

Deskripsi:
Membaca sekumpulan ulasan pelanggan dari file data/ulasan.txt baris demi baris.
Model LLM menganalisis sentimen, mendeteksi kata kunci, mengekstrak entitas bernama (NER),
dan menghasilkan ringkasan dalam format JSON terstruktur (JSON Mode).
Hasil analisis disimpan ke dalam file output/hasil_analisis.json.

Cara Menjalankan:
    python 03_text_analysis.py
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


def analyze(client, deployment: str, review: str) -> dict:
    response = client.chat.completions.create(
        model=deployment,
        messages=[{"role": "user", "content": PROMPT.format(review=review)}],
        temperature=0,
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)


def main():
    print("=" * 60)
    print("Modul 03: Analisis Teks Berstruktur (AI-901)")
    print("=" * 60)

    client = openai_client()
    deployment = env("AZURE_AI_CHAT_DEPLOYMENT")

    input_file = os.path.join("data", "ulasan.txt")
    if not os.path.exists(input_file):
        raise SystemExit(f"[ERROR] File input tidak ditemukan: {input_file}")

    with open(input_file, encoding="utf-8") as f:
        reviews = [line.strip() for line in f if line.strip()]

    print(f"Menganalisis {len(reviews)} ulasan dari {input_file}...\n")
    results = []
    for i, review in enumerate(reviews, start=1):
        try:
            data = analyze(client, deployment, review)
            sentiment = data.get("sentiment", "unknown")
            summary = data.get("summary", "")
            print(f"[{i:02d}] Sentimen: {sentiment:<8} | Ringkasan: {summary}")
        except json.JSONDecodeError:
            data = {"error": "output model bukan format JSON valid"}
            print(f"[{i:02d}] ERROR: Gagal mem-parsing format JSON")
        except Exception as e:
            data = {"error": str(e)}
            print(f"[{i:02d}] ERROR: {e}")

        results.append({"no": i, "ulasan": review, "hasil": data})

    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    out_path = os.path.join(output_dir, "hasil_analisis.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Analisis selesai. Hasil lengkap disimpan di: {out_path}")


if __name__ == "__main__":
    main()
