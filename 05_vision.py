"""
P-L2.8: Interpretasi gambar dengan model multimodal, lalu pembuatan gambar.

Siapkan foto dummy di folder data/ (misalnya data/rak.jpg).
Bagian 2 (generasi gambar) memerlukan deployment model image generation.
"""
import base64
import os
from common import env, openai_client

IMAGE_PATH = os.path.join("data", "rak.jpg")
QUESTION = "Ada berapa produk di gambar ini? Jelaskan secara singkat isinya."


def describe_image(client, deployment, path, question):
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
        temperature=0,
        max_tokens=300,
    )
    return response.choices[0].message.content


def generate_image(client, deployment, prompt, out_path):
    # [VERIFY] Parameter size/response_format bisa berbeda antar model image generation.
    result = client.images.generate(model=deployment, prompt=prompt, size="1024x1024", n=1)
    image_b64 = result.data[0].b64_json
    os.makedirs("output", exist_ok=True)
    with open(out_path, "wb") as f:
        f.write(base64.b64decode(image_b64))
    print(f"Gambar disimpan: {out_path}")


def main():
    client = openai_client()

    print("== Bagian 1: interpretasi gambar ==")
    print(describe_image(client, env("AZURE_AI_VISION_DEPLOYMENT"), IMAGE_PATH, QUESTION))

    print("\n== Bagian 2: pembuatan gambar ==")
    if os.getenv("AZURE_AI_IMAGE_DEPLOYMENT"):
        generate_image(
            client,
            env("AZURE_AI_IMAGE_DEPLOYMENT"),
            "Ilustrasi flat sederhana, tas belanja hijau di atas meja kayu, latar putih",
            os.path.join("output", "ilustrasi.png"),
        )
    else:
        print("Lewati: AZURE_AI_IMAGE_DEPLOYMENT belum diisi.")


if __name__ == "__main__":
    main()
