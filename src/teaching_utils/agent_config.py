"""
Shared Agent Configuration for Microsoft Agent Framework

Provides centralized configuration and utilities for creating and managing
Azure OpenAI agents throughout the PDF-to-Skills pipeline.
"""

import os
import sys
from pathlib import Path
from typing import Optional
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from rich.console import Console
from agent_framework import ChatAgent
from agent_framework.azure import AzureOpenAIChatClient
from azure.identity.aio import AzureCliCredential, DefaultAzureCredential


console = Console()


class AgentConfiguration:
    """Centralized configuration for Azure OpenAI agents"""

    def __init__(self, env_file: Optional[Path] = None):
        """
        Initialize agent configuration from environment variables.

        Args:
            env_file: Path to .env file. Defaults to .env.local in project root
        """
        # Load environment variables
        if env_file is None:
            project_root = Path(__file__).parent.parent.parent
            env_file = project_root / ".env.local"

        if env_file.exists():
            load_dotenv(env_file)
        else:
            console.print(f"[yellow]Warning: {env_file} not found[/yellow]")

        # Azure OpenAI configuration
        self.api_key = os.getenv("AZURE_API_KEY")
        self.endpoint = os.getenv("AZURE_ENDPOINT")
        self.api_version = os.getenv("AZURE_API_VERSION", "2025-04-01-preview")
        self.deployment = os.getenv("AZURE_CHAT_DEPLOYMENT_NAME", "gpt-4o")

        # Validate required settings
        if not self.endpoint:
            console.print("[red]Error: AZURE_ENDPOINT must be set in .env.local[/red]")
            console.print("Please copy .env.local.template to .env.local and configure")
            sys.exit(1)

        # Optional: API key (if not using managed identity)
        self.use_managed_identity = not self.api_key

        # Pipeline configuration
        self.chunk_size = int(os.getenv("PDF_CHUNK_SIZE", "8000"))
        self.max_concurrent_agents = int(os.getenv("MAX_CONCURRENT_AGENTS", "5"))
        self.checkpoint_dir = Path(os.getenv(
            "CHECKPOINT_DIR",
            str(Path(__file__).parent.parent.parent / "references" / "_checkpoints")
        ))

        # Ensure checkpoint directory exists
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def get_credential(self):
        """
        Get appropriate Azure credential based on configuration.

        Returns:
            Azure credential object (sync version)
        """
        if self.api_key:
            from azure.core.credentials import AzureKeyCredential
            return AzureKeyCredential(self.api_key)
        else:
            from azure.identity import DefaultAzureCredential as SyncDefaultAzureCredential
            return SyncDefaultAzureCredential()

    @asynccontextmanager
    async def get_async_credential(self):
        """
        Get async Azure credential as context manager.

        Yields:
            Async Azure credential object
        """
        if self.api_key:
            # For API key, use sync credential (no async needed)
            from azure.core.credentials import AzureKeyCredential
            yield AzureKeyCredential(self.api_key)
        else:
            # For managed identity, use async credential
            async with DefaultAzureCredential() as credential:
                yield credential

    def create_chat_client(self) -> AzureOpenAIChatClient:
        """
        Create Azure OpenAI chat client for agent creation.

        Returns:
            Configured AzureOpenAIChatClient instance
        """
        credential = self.get_credential()
        return AzureOpenAIChatClient(credential=credential)

    @asynccontextmanager
    async def create_agent(
        self,
        instructions: str,
        name: str,
        tools: Optional[list] = None
    ):
        """
        Create a ChatAgent with proper async context management.

        Args:
            instructions: System instructions for the agent
            name: Agent name for identification
            tools: Optional list of tool functions

        Yields:
            Configured ChatAgent instance
        """
        # ALWAYS use API key approach - simpler and more reliable
        # The framework expects api_key parameter, not credential object
        chat_client = AzureOpenAIChatClient(
            api_key=self.api_key,
            endpoint=self.endpoint,
            deployment_name=self.deployment,
            api_version=self.api_version
        )

        agent_kwargs = {
            "chat_client": chat_client,
            "instructions": instructions,
            "name": name
        }

        if tools:
            agent_kwargs["tools"] = tools

        async with ChatAgent(**agent_kwargs) as agent:
            yield agent

    def print_configuration(self):
        """Print current configuration (for debugging)"""
        console.print("[bold cyan]Agent Configuration:[/bold cyan]")
        console.print(f"Endpoint: {self.endpoint}")
        console.print(f"Model: {self.deployment}")
        console.print(f"API Version: {self.api_version}")
        console.print(f"Using Managed Identity: {self.use_managed_identity}")
        console.print(f"Chunk Size: {self.chunk_size}")
        console.print(f"Max Concurrent Agents: {self.max_concurrent_agents}")
        console.print(f"Checkpoint Directory: {self.checkpoint_dir}")


# Global configuration instance (lazy initialization)
_config: Optional[AgentConfiguration] = None


def get_config() -> AgentConfiguration:
    """
    Get global agent configuration (singleton pattern).

    Returns:
        Shared AgentConfiguration instance
    """
    global _config
    if _config is None:
        _config = AgentConfiguration()
    return _config


def reset_config():
    """Reset global configuration (useful for testing)"""
    global _config
    _config = None
