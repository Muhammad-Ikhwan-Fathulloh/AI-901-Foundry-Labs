"""
Helper bersama untuk modul Azure AI (AI-901).
Mengelola pembacaan konfigurasi environment dan inisialisasi Azure AI Project & OpenAI Client.
"""
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

# Muat variabel environment dari file .env
load_dotenv()


def env(name: str, default: str = None) -> str:
    """Mengambil nilai environment variable. Menghentikan program jika wajib tapi kosong atau masih placeholder."""
    value = os.getenv(name, default)
    if not value or value.startswith("<"):
        raise SystemExit(
            f"[ERROR] Variabel '{name}' belum diisi atau masih berupa placeholder di file .env.\n"
            f"Silakan periksa dan perbarui konfigurasi file .env Anda."
        )
    return value


def project_client() -> AIProjectClient:
    """Menginisialisasi AIProjectClient menggunakan DefaultAzureCredential."""
    endpoint = env("AZURE_AI_PROJECT_ENDPOINT")
    return AIProjectClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential(),
    )


def openai_client():
    """Mengembalikan OpenAI client yang terhubung ke Azure AI Foundry."""
    return project_client().get_openai_client()
