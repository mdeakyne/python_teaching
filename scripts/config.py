"""Azure OpenAI configuration management."""

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv


@dataclass
class AzureConfig:
    """Azure OpenAI configuration."""

    api_key: str
    endpoint: str
    api_version: str
    chat_model: str
    mini_model: str
    embedding_model: str

    @classmethod
    def from_env(cls, env_file: str = ".env.local") -> "AzureConfig":
        """Load configuration from environment file.

        Args:
            env_file: Path to .env file (default: .env.local in scripts/)

        Returns:
            AzureConfig instance

        Raises:
            ValueError: If required environment variables are missing
        """
        # Load from scripts/.env.local
        env_path = Path(__file__).parent / env_file
        load_dotenv(env_path)

        # Required variables
        required = {
            "AZURE_API_KEY": os.getenv("AZURE_API_KEY"),
            "AZURE_ENDPOINT": os.getenv("AZURE_ENDPOINT"),
            "AZURE_API_VERSION": os.getenv("AZURE_API_VERSION"),
            "AZURE_CHAT_DEPLOYMENT_NAME": os.getenv("AZURE_CHAT_DEPLOYMENT_NAME"),
            "AZURE_MINI_DEPLOYMENT_NAME": os.getenv("AZURE_MINI_DEPLOYMENT_NAME"),
            "AZURE_EMBEDDING_DEPLOYMENT": os.getenv("AZURE_EMBEDDING_DEPLOYMENT"),
        }

        # Check for missing variables
        missing = [k for k, v in required.items() if v is None]
        if missing:
            raise ValueError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

        return cls(
            api_key=required["AZURE_API_KEY"],
            endpoint=required["AZURE_ENDPOINT"],
            api_version=required["AZURE_API_VERSION"],
            chat_model=required["AZURE_CHAT_DEPLOYMENT_NAME"],
            mini_model=required["AZURE_MINI_DEPLOYMENT_NAME"],
            embedding_model=required["AZURE_EMBEDDING_DEPLOYMENT"],
        )
