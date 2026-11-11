# Panduan Praktik AI Model Alternatif (Non-Azure)

Modul alternatif ini dirancang agar siapa saja dapat mempelajari dan mempraktikkan konsep AI tingkat lanjut (Chat, Structured Output/JSON, Speech AI, Vision Multimodal) **tanpa ketergantungan pada langganan atau kuota Azure**.

---

## ❓ Apakah Bisa Menggunakan Model AI Lainnya?

**Bisa, 100%!**

Hampir seluruh ekosistem AI modern telah mengadopsi standar **OpenAI Chat Completion API Specification**. Standar ini mencakup format pengiriman prompt (`messages=[{"role": ..., "content": ...}]`), streaming, tool/function calling, format keluaran JSON (`json_object`), hingga input multimodal (URL/Base64 image).

Oleh karena itu, modul ini menyediakan adapter fleksibel (`config_alt.py`) yang memungkinkan Anda beralih antar penyedia AI hanya dengan mengubah konfigurasi file `.env`.

---

## 🚀 Pilihan Penyedia Model Alternatif

| Penyedia (Provider) | Jenis Model | Kelebihan | Biaya |
|---|---|---|---|
| **Ollama** | Llama 3.2, Mistral, DeepSeek-R1, LLaVA | Berjalan 100% lokal, offline, data privat | **Gratis (0 IDR)** |
| **OpenAI Direct** | GPT-4o, GPT-4o-mini, DALL-E 3 | Akurasi sangat tinggi, model standar industri | Berbayar per token (ada tier murah) |
| **Google Gemini** | Gemini 1.5 Flash, Gemini 2.0 Flash | Kecepatan tinggi, context window panjang (1M) | **Gratis** (tersedia kuota free di Google AI Studio) |
| **Edge-TTS & Whisper** | Microsoft Neural Voice & Whisper | Sintesis suara alami berbahasa Indonesia & STT | **Gratis (0 IDR)** tanpa API Key |

---

## 🛠️ Cara Penggunaan & Setup

### Opsi A: Menggunakan Ollama (100% Gratis & Lokal)

1. Unduh dan pasang Ollama dari [https://ollama.com](https://ollama.com).
2. Buka terminal lalu unduh model yang dibutuhkan:
   ```bash
   ollama pull llama3.2
   ollama pull llava
   ```
3. Atur di file `.env`:
   ```env
   AI_PROVIDER=ollama
   OLLAMA_BASE_URL=http://localhost:11434/v1
   OLLAMA_CHAT_MODEL=llama3.2
   OLLAMA_VISION_MODEL=llava
   ```

### Opsi B: Menggunakan Google Gemini

1. Dapatkan API Key gratis di [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Atur di file `.env`:
   ```env
   AI_PROVIDER=gemini
   GEMINI_API_KEY=AIzaSy...
   GEMINI_CHAT_MODEL=gemini-1.5-flash
   GEMINI_VISION_MODEL=gemini-1.5-flash
   ```

### Opsi C: Menggunakan OpenAI Langsung

1. Dapatkan API Key dari [OpenAI Platform](https://platform.openai.com/api-keys).
2. Atur di file `.env`:
   ```env
   AI_PROVIDER=openai
   OPENAI_API_KEY=sk-...
   OPENAI_CHAT_MODEL=gpt-4o-mini
   OPENAI_VISION_MODEL=gpt-4o-mini
   ```

---

## 🏃 Menjalankan Skrip Alternatif

```bash
# 1. Chat Client interaktif
python alternatif/01_chat_alt.py

# 2. Analisis Sentimen & Entitas (JSON Mode)
python alternatif/03_text_analysis_alt.py

# 3. Layanan Suara Gratis (Edge-TTS & Whisper)
python alternatif/04_speech_free_alt.py

# 4. Multimodal Vision (Analisis Gambar rak.jpg)
python alternatif/05_vision_alt.py
```
