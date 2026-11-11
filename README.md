# Kode Praktik AI-901, Day 2

Kode ini dipakai untuk lab Day 2 (L2.3, L2.5, L2.6, L2.7, L2.8, L2.9).

## Persiapan

1. Buat virtual environment dan install paket:

   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. Salin `.env.example` menjadi `.env`, lalu isi nilainya dari portal Azure dan Foundry.
3. Pastikan model chat (dan model multimodal jika dipakai) sudah di-deploy di Foundry.
4. Buat satu foto dummy di `data/rak.jpg` untuk L2.8.

## Urutan Praktik

| File | Lab | Yang perlu sudah tersedia |
|---|---|---|
| `01_chat_client.py` | L2.3 | Deployment model chat |
| `02_agent_client.py` | L2.5 | Agen dari L2.4 di portal |
| `03_text_analysis.py` | L2.6 | Deployment model chat, `data/ulasan.txt` |
| `04_speech.py` | L2.7 | Azure Speech resource |
| `05_vision.py` | L2.8 | Model multimodal, foto di `data/rak.jpg`, opsional model image generation |
| `06_content_understanding.py` | L2.9 | Content Understanding resource |

## Catatan untuk Trainer

- **Verifikasi sebelum sesi.** Nama paket dan method SDK berubah. Jalankan setiap file sekali dengan akun trainer. Pada `02_agent_client.py` dan `05_vision.py`, bagian yang bertanda `[VERIFY]` perlu dicek paling teliti.
- **Biaya.** Hapus deployment dan resource setelah sesi. File ini tidak mengatur budget, jadi atur alert di Cost Management.
- **Data.** Semua data di folder `data/` adalah dummy. Jangan memakai data pelanggan asli.
- **Content Understanding untuk file lokal.** Contoh di `06_content_understanding.py` memakai URL. Untuk file lokal, kirim isi file sebagai binary dengan Content-Type yang sesuai, atau gunakan SDK `azure-ai-contentunderstanding` yang sudah tersedia untuk Python.
- **Video.** Analisis video dengan Content Understanding mengikuti pola yang sama, tetapi perlu analyzer yang sesuai. Cek dokumentasi analyzer prebuilt untuk video sebelum praktik.
