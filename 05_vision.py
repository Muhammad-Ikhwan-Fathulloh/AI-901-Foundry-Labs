"""
Modul 05: Computer Vision Multimodal (Analisis Gambar & Generasi Gambar).

Deskripsi:
Bagian 1: Analisis gambar menggunakan model multimodal (Vision-LLM) untuk memahami konten gambar (data/rak.jpg).
Bagian 2: Pembuatan gambar baru (Text-to-Image) menggunakan prompt deskriptif.

Cara Menjalankan:
    python 05_vision.py
"""
import base64
import os
from common import env, openai_client

IMAGE_PATH = os.path.join("data", "rak.jpg")
QUESTION = "Ada berapa produk di gambar ini? Jelaskan secara singkat produk apa saja yang terlihat."


def describe_image(client, deployment: str, path: str, question: str) -> str:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File gambar tidak ditemukan di: {path}")

    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")

    response = client.chat.completions.create(
        model=deployment,
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


def generate_image(client, deployment: str, prompt: str, out_path: str):
    print(f"Men-generate gambar baru dengan prompt: '{prompt}'...")
    result = client.images.generate(model=deployment, prompt=prompt, size="1024x1024", n=1)
    image_b64 = result.data[0].b64_json

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(base64.b64decode(image_b64))
    print(f"[OK] Gambar berhasil disimpan di: {out_path}")


def main():
    print("=" * 60)
    print("Modul 05: Computer Vision Multimodal (AI-901)")
    print("=" * 60)

    client = openai_client()

    print("\n== Bagian 1: Analisis Gambar Multimodal ==")
    vision_deployment = env("AZURE_AI_VISION_DEPLOYMENT")
    try:
        description = describe_image(client, vision_deployment, IMAGE_PATH, QUESTION)
        print(f"File Gambar: {IMAGE_PATH}")
        print(f"Pertanyaan : {QUESTION}")
        print(f"Hasil Analisis:\n{description}")
    except Exception as e:
        print(f"[ERROR] Gagal menganalisis gambar: {e}")

    print("\n== Bagian 2: Pembuatan Gambar (Text-to-Image) ==")
    image_deployment = os.getenv("AZURE_AI_IMAGE_DEPLOYMENT")
    if image_deployment and not image_deployment.startswith("<"):
        try:
            generate_image(
                client,
                image_deployment,
                "Ilustrasi flat sederhana, tas belanja ramah lingkungan berwarna hijau di atas meja kayu, latar putih",
                os.path.join("output", "ilustrasi.png"),
            )
        except Exception as e:
            print(f"[ERROR] Gagal generate gambar: {e}")
    else:
        print("[INFO] Lewati Bagian 2: AZURE_AI_IMAGE_DEPLOYMENT belum diisi di .env (opsional).")


if __name__ == "__main__":
    main()
