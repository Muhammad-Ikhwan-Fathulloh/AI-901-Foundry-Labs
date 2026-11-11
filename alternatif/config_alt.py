"""
Helper & Factory Klien Multi-Provider untuk Model Alternatif.
Mendukung:
1. Ollama (Lokal, Gratis, Offline)
2. Direct OpenAI (Cloud)
3. Google Gemini (Cloud via OpenAI Compatibility Endpoint)
"""
import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_provider() -> str:
    """Mengambil nama provider yang aktif (default: ollama)."""
    return os.getenv("AI_PROVIDER", "ollama").lower()


def get_model_name(task_type: str = "chat") -> str:
    """
    Mengambil nama model berdasarkan provider dan jenis tugas.
    task_type: 'chat', 'vision', atau 'json'
    """
    provider = get_provider()

    if provider == "ollama":
        if task_type == "vision":
            return os.getenv("OLLAMA_VISION_MODEL", "llava")
        return os.getenv("OLLAMA_CHAT_MODEL", "llama3.2")
    elif provider == "openai":
        if task_type == "vision":
            return os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini")
        return os.getenv("OPENAI_CHAT_MODEL", "gpt-4o-mini")
    elif provider == "gemini":
        if task_type == "vision":
            return os.getenv("GEMINI_VISION_MODEL", "gemini-1.5-flash")
        return os.getenv("GEMINI_CHAT_MODEL", "gemini-1.5-flash")
    else:
        return os.getenv("CUSTOM_MODEL_NAME", "llama3.2")


def get_alternative_client() -> OpenAI:
    """
    Membuat klien OpenAI SDK yang diarahkan ke provider pilihan.
    """
    provider = get_provider()

    if provider == "ollama":
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
        # Ollama tidak memerlukan autentikasi API key riil
        return OpenAI(base_url=base_url, api_key="ollama")

    elif provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key.startswith("<"):
            raise SystemExit("[ERROR] OPENAI_API_KEY belum diisi di file .env")
        return OpenAI(api_key=api_key)

    elif provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key or api_key.startswith("<"):
            raise SystemExit("[ERROR] GEMINI_API_KEY belum diisi di file .env")
        # Google Gemini menyediakan OpenAI Compatibility Endpoint
        return OpenAI(
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
            api_key=api_key,
        )

    else:
        raise ValueError(f"Provider '{provider}' tidak dikenal. Pilih: ollama, openai, atau gemini.")
