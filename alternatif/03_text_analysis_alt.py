"""
Alternatif 03: Analisis Teks Berstruktur (JSON Mode) dengan Model Alternatif.
Mendukung ekstraksi sentimen, kata kunci, entitas, dan ringkasan dari data/ulasan.txt.

Cara Menjalankan:
    python alternatif/03_text_analysis_alt.py
"""
import json
import os
import sys

sys.path.append(os.path.dirname(__file__))
from config_alt import get_alternative_client, get_model_name, get_provider

PROMPT = """Analisis ulasan berikut. Balas HANYA dengan JSON valid dengan kunci:
- "keywords": daftar kata kunci (string)
- "entities": daftar objek {"text": ..., "type": "product|location|brand|person|other"}
- "sentiment": salah satu dari "positive", "negative", "neutral", "mixed"
- "summary": satu kalimat dalam bahasa Indonesia

Ulasan: \"\"\"{review}\"\"\""""


def analyze(client, model: str, review: str) -> dict:
    # Menggunakan response_format json_object untuk menjamin validitas output JSON
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": PROMPT.format(review=review)}],
        temperature=0,
        response_format={"type": "json_object"},
    )
    return json.loads(response.choices[0].message.content)


def main():
    provider = get_provider()
    model = get_model_name("chat")

    print("=" * 60)
    print("Modul Alternatif 03: Analisis Teks Berstruktur (JSON Mode)")
    print(f"Provider Terpilih : {provider.upper()}")
    print(f"Model Digunakan   : {model}")
    print("=" * 60)

    try:
        client = get_alternative_client()
    except Exception as e:
        print(f"[ERROR] Inisialisasi klien gagal: {e}")
        return

    input_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "ulasan.txt")
    if not os.path.exists(input_file):
        raise SystemExit(f"[ERROR] File input tidak ditemukan: {input_file}")

    with open(input_file, encoding="utf-8") as f:
        reviews = [line.strip() for line in f if line.strip()]

    print(f"Menganalisis {len(reviews)} ulasan...\n")
    results = []

    for i, review in enumerate(reviews, start=1):
        try:
            data = analyze(client, model, review)
            sentiment = data.get("sentiment", "unknown")
            summary = data.get("summary", "")
            print(f"[{i:02d}] Sentimen: {sentiment:<8} | Ringkasan: {summary}")
        except json.JSONDecodeError:
            data = {"error": "output model bukan format JSON valid"}
            print(f"[{i:02d}] ERROR: Output tidak sesuai format JSON")
        except Exception as e:
            data = {"error": str(e)}
            print(f"[{i:02d}] ERROR: {e}")

        results.append({"no": i, "ulasan": review, "hasil": data})

    out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "hasil_analisis_alt.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Analisis selesai. Hasil disimpan di: {out_path}")


if __name__ == "__main__":
    main()
