"""Helper bersama: memuat .env dan membuat client Foundry."""
import os
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

load_dotenv()


def env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise SystemExit(f"Variabel {name} belum diisi di file .env")
    return value


def project_client() -> AIProjectClient:
    return AIProjectClient(
        endpoint=env("AZURE_AI_PROJECT_ENDPOINT"),
        credential=DefaultAzureCredential(),
    )


def openai_client():
    return project_client().get_openai_client()
