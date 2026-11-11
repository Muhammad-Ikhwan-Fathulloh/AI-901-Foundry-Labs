"""
P-L2.9: Ekstraksi informasi dengan Azure Content Understanding (REST API).

Alur: kirim file -> dapat Operation-Location -> polling sampai selesai -> cetak hasil.
Contoh memakai prebuilt-invoice dan file invoice contoh dari URL publik.
Untuk file lokal atau video, lihat catatan di README.md.
"""
import json
import os
import time
import requests
from dotenv import load_dotenv

load_dotenv()

API_VERSION = "2025-11-01"
ANALYZER_ID = "prebuilt-invoice"
SAMPLE_URL = "https://github.com/Azure-Samples/azure-ai-content-understanding-python/raw/refs/heads/main/data/invoice.pdf"


def headers():
    return {
        "Ocp-Apim-Subscription-Key": os.environ["CU_KEY"],
        "Content-Type": "application/json",
    }


def start_analysis(endpoint, analyzer_id, url):
    api = f"{endpoint}/contentunderstanding/analyzers/{analyzer_id}:analyze?api-version={API_VERSION}"
    r = requests.post(api, headers=headers(), json={"inputs": [{"url": url}]}, timeout=60)
    r.raise_for_status()
    return r.headers["Operation-Location"]


def poll(operation_url, timeout_s=180):
    start = time.time()
    while time.time() - start < timeout_s:
        r = requests.get(operation_url, headers=headers(), timeout=60)
        r.raise_for_status()
        body = r.json()
        status = body.get("status", "").lower()
        if status == "succeeded":
            return body
        if status in ("failed", "cancelled"):
            raise SystemExit(f"Analisis gagal: {json.dumps(body, ensure_ascii=False)}")
        time.sleep(3)
    raise SystemExit("Waktu tunggu habis.")


def main():
    endpoint = os.environ["CU_ENDPOINT"].rstrip("/")
    operation_url = start_analysis(endpoint, ANALYZER_ID, SAMPLE_URL)
    result = poll(operation_url)

    os.makedirs("output", exist_ok=True)
    out_path = os.path.join("output", "hasil_invoice.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
    print(f"Hasil disimpan di {out_path}")
    print("Lihat bagian 'fields' di dalam file untuk nomor invoice, tanggal, dan total.")


if __name__ == "__main__":
    main()
