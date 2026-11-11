"""
Alternatif 06: Document Understanding & Ekstraksi Invoice Terstruktur.

Deskripsi:
Mengekstrak informasi penting dari dokumen invoice PDF (data/invoice.pdf)
tanpa memerlukan layanan berbayar Azure Content Understanding.
Mendukung:
1. Ekstraksi teks PDF menggunakan library lokal (pypdf / pdfplumber)
2. Analisis & konversi ke skema JSON terstruktur menggunakan:
   - Google Gemini (Free tier)
   - Ollama (Lokal & Gratis: Llama 3.2 / Qwen 2.5)
   - OpenAI Direct (GPT-4o-mini)

Cara Menjalankan:
    python alternatif/06_documents_alt.py
"""
import json
import os
import sys

sys.path.append(os.path.dirname(__file__))
from config_alt import get_alternative_client, get_model_name, get_provider

PDF_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "invoice.pdf")

EXTRACT_PROMPT = """Anda adalah sistem Content Understanding / Document Intelligence AI.
Analisis isi teks dokumen invoice berikut, lalu ekstrak field menjadi format JSON valid HANYA dengan struktur:
{
  "vendor_name": "Nama perusahaan penerbit invoice",
  "vendor_address": "Alamat vendor",
  "customer_name": "Nama pembeli / klien",
  "invoice_number": "Nomor invoice",
  "invoice_date": "Tanggal invoice",
  "due_date": "Batas waktu pembayaran",
  "items": [
    {
      "description": "Deskripsi item/jasa",
      "quantity": 1,
      "unit_price": 0.0,
      "amount": 0.0
    }
  ],
  "subtotal": 0.0,
  "tax": 0.0,
  "total_amount": 0.0
}

Teks Dokumen Invoice:
\"\"\"{document_text}\"\"\""""


def baca_teks_pdf(path_pdf: str) -> str:
    """Mengekstrak seluruh teks dari file PDF menggunakan pypdf atau pdfplumber."""
    if not os.path.exists(path_pdf):
        raise FileNotFoundError(f"File PDF tidak ditemukan: {path_pdf}")

    try:
        import pypdf
        reader = pypdf.PdfReader(path_pdf)
        teks = "\n".join([page.extract_text() or "" for page in reader.pages])
        if teks.strip():
            return teks
    except ImportError:
        pass

    try:
        import pdfplumber
        with pdfplumber.open(path_pdf) as pdf:
            return "\n".join([page.extract_text() or "" for page in pdf.pages])
    except ImportError:
        pass

    raise RuntimeError("Silakan pasang 'pypdf' atau 'pdfplumber' untuk membaca file PDF: pip install pypdf")


def ekstrak_invoice(client, model: str, teks_dokumen: str) -> dict:
    """Mengirim teks invoice ke model LLM untuk ekstraksi JSON terstruktur."""
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": EXTRACT_PROMPT.format(document_text=teks_dokumen)}],
        temperature=0,
        response_format={"type": "json_object"}
    )
    return json.loads(response.choices[0].message.content)


def main():
    provider = get_provider()
    model = get_model_name("chat")

    print("=" * 60)
    print("Modul Alternatif 06: Document Understanding (Invoice Extractor)")
    print(f"Provider Terpilih : {provider.upper()}")
    print(f"Model Digunakan   : {model}")
    print("=" * 60)

    try:
        client = get_alternative_client()
    except Exception as e:
        print(f"[ERROR] Inisialisasi klien gagal: {e}")
        return

    print(f"\n1. Membaca file PDF: {PDF_PATH}")
    teks_pdf = baca_teks_pdf(PDF_PATH)
    print(f"   [OK] Teks berhasil diekstrak ({len(teks_pdf)} karakter).")

    print("\n2. Mengekstrak field dokumen ke format JSON terstruktur...")
    try:
        data_invoice = ekstrak_invoice(client, model, teks_pdf)
        print("   [OK] Ekstraksi berhasil!\n")

        print("--- Ringkasan Dokumen Invoice ---")
        print(f"Vendor        : {data_invoice.get('vendor_name', '-')}")
        print(f"Customer      : {data_invoice.get('customer_name', '-')}")
        print(f"No. Invoice   : {data_invoice.get('invoice_number', '-')}")
        print(f"Tanggal       : {data_invoice.get('invoice_date', '-')}")
        print(f"Total Tagihan : {data_invoice.get('total_amount', '-')}")
        print("Items         :")
        for item in data_invoice.get("items", []):
            print(f"  - {item.get('description', '')} (Qty: {item.get('quantity', '')}) : {item.get('amount', '')}")

        out_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, "hasil_invoice_alt.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data_invoice, f, ensure_ascii=False, indent=2)

        print(f"\n[OK] Hasil ekstraksi JSON lengkap disimpan di: {out_path}")

    except Exception as e:
        print(f"[ERROR Ekstraksi]: {e}")


if __name__ == "__main__":
    main()
