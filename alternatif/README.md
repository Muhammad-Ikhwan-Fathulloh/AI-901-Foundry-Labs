# Panduan Praktik AI Model Alternatif (Non-Azure)

Modul alternatif ini dirancang agar siapa saja dapat mempelajari dan mempraktikkan seluruh konsep silabus **AI-901 (Chat, Agents, Text Analysis, Speech, Vision, & Document Understanding)** **tanpa ketergantungan pada langganan atau kuota Azure**.

---

## 📊 Matriks Keselarasan Modul (Azure vs Alternatif)

Berikut adalah pemetaan lengkap antara modul Azure resmi dan implementasi alternatif gratis/lokal yang tersedia di repositori ini:

| Modul Ujian / Topik | Target Azure | Alternatif Free Cloud (Gemini) | Alternatif Offline (Ollama/Lokal) | Skrip Alternatif |
|---|---|---|---|---|
| **01. Chat LLM** | Azure OpenAI (GPT-4o) | `gemini-1.5-flash` | `llama3.2` | [`01_chat_alt.py`](01_chat_alt.py) |
| **02. AI Agents** | Azure AI Agent Service | Gemini Function Calling | Ollama Tool Calling | [`02_agent_alt.py`](02_agent_alt.py) |
| **03. Text Analysis** | Azure Language / JSON Mode | Gemini JSON Mode | Llama 3.2 JSON Mode | [`03_text_analysis_alt.py`](03_text_analysis_alt.py) |
| **04. Speech AI** | Azure Speech Service | Edge-TTS (TTS) + Whisper (STT) | Edge-TTS (TTS) + Whisper (STT) | [`04_speech_free_alt.py`](04_speech_free_alt.py) |
| **05. Vision** | Azure OpenAI Vision | Gemini 1.5 Flash Multimodal | LLaVA / Llama 3.2 Vision | [`05_vision_alt.py`](05_vision_alt.py) |
| **06. Documents** | Content Understanding | Gemini Document Analysis | pypdf + Llama 3.2 Extractor | [`06_documents_alt.py`](06_documents_alt.py) |

---

## ❓ Mengapa Bisa Menggunakan Model Lain?

Hampir seluruh ekosistem AI modern telah mengadopsi standar antarmuka **OpenAI Specification**:
1. Format pesan standar: `messages=[{"role": ..., "content": ...}]`
2. **Tool/Function Calling:** format skema JSON untuk memanggil fungsi lokal secara otonom.
3. **Structured Outputs (JSON Mode):** `response_format={"type": "json_object"}` untuk menjamin keluaran JSON valid.
4. **Multimodal Input:** format pengiriman gambar URL/Base64 langsung ke model LLM.

Melalui adapter [`config_alt.py`](config_alt.py), Anda dapat beralih penyedia model secara instan hanya dengan mengubah variabel `AI_PROVIDER` di file `.env`.

---

## 🛠️ Pilihan Setup & Konfigurasi

### Opsi A: Menggunakan Google Gemini (Free Cloud - Rekomendasi)
1. Dapatkan API Key gratis di [Google AI Studio](https://aistudio.google.com/app/apikey).
2. Atur di file `.env`:
   ```env
   AI_PROVIDER=gemini
   GEMINI_API_KEY=AIzaSy...IsiKunciAnda...
   GEMINI_CHAT_MODEL=gemini-1.5-flash
   GEMINI_VISION_MODEL=gemini-1.5-flash
   ```

### Opsi B: Menggunakan Ollama (100% Offline & Lokal)
1. Pasang Ollama dari [https://ollama.com](https://ollama.com).
2. Unduh model di terminal:
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

### Opsi C: Menggunakan OpenAI Langsung
1. Dapatkan API Key di [OpenAI Platform](https://platform.openai.com/api-keys).
2. Atur di file `.env`:
   ```env
   AI_PROVIDER=openai
   OPENAI_API_KEY=sk-...
   OPENAI_CHAT_MODEL=gpt-4o-mini
   OPENAI_VISION_MODEL=gpt-4o-mini
   ```

---

## 🏃 Cara Menjalankan Seluruh Modul Alternatif

```bash
# 01. Chat Client Interaktif multi-turn
python alternatif/01_chat_alt.py

# 02. Autonomous AI Agent dengan Tool Calling (cek ongkir & resi)
python alternatif/02_agent_alt.py

# 03. Analisis Teks Berstruktur (Sentimen, Entitas NER, Ringkasan)
python alternatif/03_text_analysis_alt.py

# 04. Layanan Suara 100% Gratis (TTS Suara Natural & STT Whisper)
python alternatif/04_speech_free_alt.py

# 05. Multimodal Vision (Analisis Foto Rak Toko)
python alternatif/05_vision_alt.py

# 06. Document Understanding (Ekstraksi Invoice PDF ke JSON)
python alternatif/06_documents_alt.py
```
