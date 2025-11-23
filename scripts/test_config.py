import os
from pathlib import Path

import pytest


def test_azure_config_loads_from_env():
    """Test that AzureConfig loads from .env.local"""
    from config import AzureConfig

    config = AzureConfig.from_env()

    assert config.api_key is not None
    assert config.endpoint is not None
    assert config.chat_model == "gpt-5-chat"
    assert config.mini_model == "gpt-5-mini"
    assert config.embedding_model == "text-embedding-3-large"


def test_azure_config_raises_on_missing_env():
    """Test that missing env vars raise clear error"""
    from config import AzureConfig

    # Save and clear all Azure env vars
    saved_vars = {}
    azure_vars = [
        "AZURE_API_KEY",
        "AZURE_ENDPOINT",
        "AZURE_API_VERSION",
        "AZURE_CHAT_DEPLOYMENT_NAME",
        "AZURE_MINI_DEPLOYMENT_NAME",
        "AZURE_EMBEDDING_DEPLOYMENT",
    ]

    for var in azure_vars:
        if var in os.environ:
            saved_vars[var] = os.environ[var]
            del os.environ[var]

    try:
        # Use a non-existent env file to ensure variables aren't loaded
        with pytest.raises(ValueError, match="AZURE_API_KEY"):
            AzureConfig.from_env(env_file=".env.nonexistent")
    finally:
        # Restore
        for var, value in saved_vars.items():
            os.environ[var] = value
