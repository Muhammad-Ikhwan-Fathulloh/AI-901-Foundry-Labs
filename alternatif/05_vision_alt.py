"""
Alternatif 05: Computer Vision Multimodal dengan Model Non-Azure.
Mendukung analisis gambar menggunakan:
- Ollama: LLaVA atau Llama 3.2 Vision (100% lokal & gratis)
- OpenAI: GPT-4o-mini
- Google Gemini: Gemini 1.5 Flash

Cara Menjalankan:
    python alternatif/05_vision_alt.py
"""
import base64
import os
import sys

sys.path.append(os.path.dirname(__file__))
from config_alt import get_alternative_client, get_model_name, get_provider

IMAGE_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "rak.jpg")
QUESTION = "Ada berapa produk di gambar ini? Jelaskan secara singkat produk apa saja yang terlihat."


def describe_image(client, model: str, path: str, question: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File gambar tidak ditemukan di: {path}")

    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    response = client.chat.completions.create(
        model=model,
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": question},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{b64}"}},
            ],
        }],
        temperature=0.2,
        max_tokens=300,
    )
    return response.choices[0].message.content


def main():
    provider = get_provider()
    model = get_model_name("vision")

    print("=" * 60)
    print("Modul Alternatif 05: Analisis Gambar Multimodal")
    print(f"Provider Terpilih : {provider.upper()}")
    print(f"Model Vision      : {model}")
    print("=" * 60)

    try:
        client = get_alternative_client()
    except Exception as e:
        print(f"[ERROR] Inisialisasi klien gagal: {e}")
        return

    print(f"\nMenganalisis gambar: {IMAGE_PATH}")
    print(f"Pertanyaan: {QUESTION}\n")

    try:
        description = describe_image(client, model, IMAGE_PATH, QUESTION)
        print("--- Hasil Analisis Vision LLM ---")
        print(description)
    except Exception as e:
        print(f"[ERROR] Gagal memproses gambar dengan model {model}: {e}")
        if provider == "ollama":
            print(f"Tips: Pastikan model vision sudah diunduh di Ollama dengan perintah: 'ollama pull {model}'.")


if __name__ == "__main__":
    main()
