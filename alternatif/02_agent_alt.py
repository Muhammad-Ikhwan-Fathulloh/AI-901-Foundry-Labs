"""
Alternatif 02: AI Agent dengan Kemampuan Tool Calling (Function Calling).

Deskripsi:
Mengimplementasikan Autonomous AI Agent yang dapat memanggil fungsi eksternal (tools)
untuk menyelesaikan tugas secara otomatis.
Kompatibel dengan:
- Ollama (Lokal): Model seperti llama3.2, mistral, qwen2.5 mendukung tool calling
- Google Gemini: Mendukung function calling via OpenAI endpoint
- OpenAI Direct: GPT-4o-mini

Cara Menjalankan:
    python alternatif/02_agent_alt.py
"""
import json
import os
import sys

sys.path.append(os.path.dirname(__file__))
from config_alt import get_alternative_client, get_model_name, get_provider

# ==============================================================================
# 1. Definisi Fungsi Nyata (Tools / Python Functions)
# ==============================================================================

def cek_ongkos_kirim(kota: str, berat_kg: float) -> str:
    """Menghitung tarif ongkos kirim berdasarkan kota dan berat barang."""
    tarif_dasar = {
        "jakarta": 10000,
        "bandung": 12000,
        "surabaya": 18000,
        "medan": 25000,
        "makassar": 30000,
    }
    kota_clean = kota.lower().strip()
    tarif_per_kg = tarif_dasar.get(kota_clean, 20000)
    total = int(tarif_per_kg * berat_kg)
    return json.dumps({
        "kota": kota.title(),
        "berat_kg": berat_kg,
        "tarif_per_kg": tarif_per_kg,
        "total_ongkir": f"Rp {total:,}".replace(",", ".")
    })


def cek_status_pesanan(nomor_pesanan: str) -> str:
    """Mengecek status pengiriman pesanan berdasarkan nomor resi/order."""
    database_pesanan = {
        "ORD-001": {"status": "Sedang Dikirim", "kurir": "JNE Express", "posisi": "Hub Jakarta Barat"},
        "ORD-002": {"status": "Dalam Proses Pengemasan", "kurir": "SiCepat", "posisi": "Gudang Pusat"},
        "ORD-003": {"status": "Telah Diterima", "kurir": "J&T", "posisi": "Diterima oleh Satpam"},
    }
    hasil = database_pesanan.get(nomor_pesanan.upper())
    if not hasil:
        return json.dumps({"error": f"Nomor pesanan '{nomor_pesanan}' tidak ditemukan."})
    return json.dumps({"nomor_pesanan": nomor_pesanan.upper(), **hasil})


# ==============================================================================
# 2. Skema Tools (OpenAI Specification)
# ==============================================================================

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "cek_ongkos_kirim",
            "description": "Menghitung estimasi ongkos kirim paket ke kota tujuan di Indonesia.",
            "parameters": {
                "type": "object",
                "properties": {
                    "kota": {
                        "type": "string",
                        "description": "Nama kota tujuan pengiriman (misal: Jakarta, Surabaya, Bandung)"
                    },
                    "berat_kg": {
                        "type": "number",
                        "description": "Berat paket dalam satuan kilogram (contoh: 1.5, 2)"
                    }
                },
                "required": ["kota", "berat_kg"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "cek_status_pesanan",
            "description": "Mengecek status terkini dan lokasi pengiriman paket berdasarkan nomor pesanan (order ID).",
            "parameters": {
                "type": "object",
                "properties": {
                    "nomor_pesanan": {
                        "type": "string",
                        "description": "Nomor pesanan pelanggan (contoh: ORD-001, ORD-002)"
                    }
                },
                "required": ["nomor_pesanan"]
            }
        }
    }
]

DAFTAR_FUNGSI = {
    "cek_ongkos_kirim": cek_ongkos_kirim,
    "cek_status_pesanan": cek_status_pesanan,
}


# ==============================================================================
# 3. Alur Eksekusi Agent (ReAct / Tool Execution Loop)
# ==============================================================================

def jalankan_agent(client, model: str, query_user: str):
    print(f"\n[User]: {query_user}")
    messages = [
        {
            "role": "system",
            "content": (
                "Anda adalah asisten cerdas layanan logistik & toko online. "
                "Gunakan tools yang tersedia untuk menjawab pertanyaan pengguna. "
                "Jawab dengan ramah dalam bahasa Indonesia."
            )
        },
        {"role": "user", "content": query_user}
    ]

    # Panggilan pertama: LLM menentukan apakah butuh tools
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        tools=TOOLS,
        tool_choice="auto"
    )
    msg = response.choices[0].message
    messages.append(msg)

    # Periksa apakah model meminta pemanggilan fungsi
    if msg.tool_calls:
        for tool_call in msg.tool_calls:
            fn_name = tool_call.function.name
            fn_args = json.loads(tool_call.function.arguments)
            print(f"  🤖 [Agent Memanggil Tool]: {fn_name}({fn_args})")

            # Eksekusi fungsi Python lokal
            fungsi = DAFTAR_FUNGSI.get(fn_name)
            if fungsi:
                hasil_tool = fungsi(**fn_args)
            else:
                hasil_tool = json.dumps({"error": f"Fungsi {fn_name} tidak ditemukan."})

            print(f"  📥 [Hasil Eksekusi Tool]: {hasil_tool}")

            # Kirim hasil eksekusi tool kembali ke LLM
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": hasil_tool
            })

        # Panggilan kedua: LLM menyusun jawaban akhir berdasarkan hasil tool
        response_akhir = client.chat.completions.create(
            model=model,
            messages=messages
        )
        jawaban_final = response_akhir.choices[0].message.content
        print(f"[Asisten]: {jawaban_final}\n")
    else:
        # Jika model tidak butuh tools
        print(f"[Asisten]: {msg.content}\n")


def main():
    provider = get_provider()
    model = get_model_name("chat")

    print("=" * 60)
    print("Modul Alternatif 02: AI Agent dengan Tool Calling")
    print(f"Provider Terpilih : {provider.upper()}")
    print(f"Model Digunakan   : {model}")
    print("=" * 60)

    try:
        client = get_alternative_client()
    except Exception as e:
        print(f"[ERROR] Inisialisasi klien gagal: {e}")
        return

    pertanyaan_uji = [
        "Halo, tolong cek ongkir ke Surabaya kalau berat paket saya 3 kg berapa ya?",
        "Pesanan saya dengan nomor ORD-001 posisinya sudah sampai mana?",
        "Apakah toko buka di hari Minggu?"
    ]

    for q in pertanyaan_uji:
        try:
            jalankan_agent(client, model, q)
        except Exception as e:
            print(f"[ERROR Agent]: {e}")
            if provider == "ollama":
                print("Tips: Pastikan model Ollama mendukung tool calling (misal: 'llama3.2', 'qwen2.5', 'mistral').")


if __name__ == "__main__":
    main()
