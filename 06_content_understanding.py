"""
Modul 06: Azure Content Understanding (Ekstraksi Dokumen Terstruktur & Invoice).

Deskripsi:
Mengirimkan dokumen invoice ke layanan Azure Content Understanding via REST API,
melakukan asynchronous polling hingga proses analisis selesai, dan menyimpan
hasil ekstraksi field (nomor invoice, tanggal, total, vendor) ke file JSON.

Pola Alur Kerja REST:
1. POST dokumen -> Terima HTTP 202 Accepted & URL polling pada header 'Operation-Location'
2. GET Operation-Location secara berkala sampai status = 'succeeded'
3. Simpan dan proses hasil ekstraksi field terstruktur

Cara Menjalankan:
    python 06_content_understanding.py
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


def get_headers():
    key = os.getenv("CU_KEY")
    if not key or key.startswith("<"):
        raise SystemExit("[ERROR] Variabel CU_KEY belum diisi di file .env")
    return {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
    }


def start_analysis(endpoint: str, analyzer_id: str, url: str) -> str:
    api = f"{endpoint}/contentunderstanding/analyzers/{analyzer_id}:analyze?api-version={API_VERSION}"
    print(f"1. Mengirim dokumen invoice ke analyzer '{analyzer_id}'...")
    r = requests.post(api, headers=get_headers(), json={"inputs": [{"url": url}]}, timeout=60)
    r.raise_for_status()

    operation_url = r.headers.get("Operation-Location")
    if not operation_url:
        raise ValueError("Header 'Operation-Location' tidak ditemukan pada respon Azure.")
    print("   [OK] Permintaan diterima Azure (HTTP 202). URL Polling diperoleh.")
    return operation_url


def poll_result(operation_url: str, timeout_s: int = 180) -> dict:
    print("2. Menunggu hasil ekstraksi (asynchronous polling)...")
    start = time.time()
    while time.time() - start < timeout_s:
        r = requests.get(operation_url, headers=get_headers(), timeout=60)
        r.raise_for_status()
        body = r.json()
        status = body.get("status", "").lower()

        if status == "succeeded":
            print("   [OK] Analisis dokumen berhasil diselesaikan!")
            return body
        if status in ("failed", "cancelled"):
            raise SystemExit(f"   [ERROR] Analisis gagal dengan status '{status}':\n{json.dumps(body, ensure_ascii=False, indent=2)}")

        time.sleep(3)
        print("   ...masih diproses...")

    raise TimeoutError(f"Waktu tunggu ({timeout_s}s) habis sebelum analisis selesai.")


def main():
    print("=" * 60)
    print("Modul 06: Azure Content Understanding (AI-901)")
    print("=" * 60)

    raw_endpoint = os.getenv("CU_ENDPOINT")
    if not raw_endpoint or raw_endpoint.startswith("<"):
        raise SystemExit("[ERROR] Variabel CU_ENDPOINT belum diisi di file .env")

    endpoint = raw_endpoint.rstrip("/")
    try:
        operation_url = start_analysis(endpoint, ANALYZER_ID, SAMPLE_URL)
        result = poll_result(operation_url)

        os.makedirs("output", exist_ok=True)
        out_path = os.path.join("output", "hasil_invoice.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=2)

        print(f"\n[OK] Hasil ekstraksi disimpan di: {out_path}")
        print("Periksa atribut 'fields' pada file JSON untuk melihat nomor invoice, tanggal, vendor, dan total biaya.")
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Kesalahan jaringan atau HTTP: {e}")
    except Exception as e:
        print(f"[ERROR] Terjadi kesalahan: {e}")


if __name__ == "__main__":
    main()
