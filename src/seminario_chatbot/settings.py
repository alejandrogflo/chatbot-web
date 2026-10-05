from dataclasses import dataclass
import os

from dotenv import load_dotenv


load_dotenv()


@dataclass(frozen=True)
class Settings:
    database_url: str | None
    groq_api_key: str | None
    groq_model: str
    secret_key: str | None


def get_settings() -> Settings:
    return Settings(
        database_url=os.getenv("DATABASE_URL"),
        groq_api_key=os.getenv("GROQ_API_KEY"),
        groq_model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
        secret_key=os.getenv("SECRET_KEY"),
    )
