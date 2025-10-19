#!/usr/bin/env python3
"""
PDF to Markdown Converter using Azure AI Foundry

Extracts text from PDF books and uses Azure AI agents to convert them
to well-structured markdown with preserved code blocks and formatting.
"""

import os
import sys
from pathlib import Path
from typing import Optional
import json

from dotenv import load_dotenv
from pypdf import PdfReader
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from azure.ai.projects.models import Agent, AgentThread, ThreadMessage
from pydantic import BaseModel


console = Console()


class BookConfig(BaseModel):
    """Configuration for a book to process"""
    filename: str
    output_name: str
    priority: int = 0
    description: str = ""


# Priority books configuration
PRIORITY_BOOKS = [
    BookConfig(
        filename="Dive Into Data Science.pdf",
        output_name="dive-into-data-science",
        priority=1,
        description="Data Science fundamentals"
    ),
    BookConfig(
        filename="Beyond the Basics with Python.pdf",
        output_name="beyond-basics-python",
        priority=1,
        description="Advanced Python for automation"
    ),
    BookConfig(
        filename="Book of Dash.pdf",
        output_name="book-of-dash",
        priority=2,
        description="Web dashboards with Dash"
    ),
    BookConfig(
        filename="Impractical Python Projects.pdf",
        output_name="impractical-python-projects",
        priority=2,
        description="Creative Python projects"
    ),
]


class AzureAIClient:
    """Wrapper for Azure AI Foundry agent interactions"""

    def __init__(self):
        load_dotenv(".env.local")

        # Get configuration from environment
        connection_string = os.getenv("AZURE_PROJECT_CONNECTION_STRING")

        if not connection_string:
            console.print("[red]Error: AZURE_PROJECT_CONNECTION_STRING not set in .env.local[/red]")
            console.print("Please copy .env.local.template to .env.local and fill in your credentials")
            sys.exit(1)

        # Initialize the Azure AI Project client
        self.client = AIProjectClient.from_connection_string(
            credential=DefaultAzureCredential(),
            conn_str=connection_string
        )

        self.agent = None
        self.thread = None

    def create_markdown_agent(self):
        """Create an agent specialized in converting PDF text to markdown"""
        console.print("[cyan]Creating Azure AI agent for markdown conversion...[/cyan]")

        self.agent = self.client.agents.create_agent(
            model=os.getenv("AZURE_AI_MODEL_DEPLOYMENT", "gpt-4"),
            name="pdf-to-markdown-converter",
            instructions="""You are an expert at converting technical book content to clean, well-structured markdown.

Your tasks:
1. Take raw PDF text and convert it to proper markdown format
2. Identify and preserve code blocks with appropriate language tags
3. Structure content with proper headings (##, ###)
4. Maintain lists, tables, and formatting
5. Clean up OCR artifacts and spacing issues
6. Preserve technical accuracy

Output only the cleaned markdown without any explanations."""
        )

        console.print(f"[green]✓ Agent created: {self.agent.id}[/green]")
        return self.agent

    def process_text_chunk(self, text: str) -> str:
        """Process a text chunk through the agent"""
        # Create a thread for this interaction
        thread = self.client.agents.create_thread()

        # Send the text to process
        message = self.client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=f"Convert this PDF text to clean markdown:\n\n{text}"
        )

        # Run the agent
        run = self.client.agents.create_and_process_run(
            thread_id=thread.id,
            agent_id=self.agent.id
        )

        # Get the response
        messages = self.client.agents.list_messages(thread_id=thread.id)

        # Extract the markdown from the last assistant message
        for msg in messages:
            if msg.role == "assistant":
                # Get the text content from the message
                if hasattr(msg, 'content') and len(msg.content) > 0:
                    return msg.content[0].text.value

        return text  # Fallback to original if processing fails


def extract_text_from_pdf(pdf_path: Path) -> list[str]:
    """Extract text from PDF, returning pages as list"""
    console.print(f"[cyan]Extracting text from {pdf_path.name}...[/cyan]")

    reader = PdfReader(pdf_path)
    pages = []

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task(
            f"Reading {len(reader.pages)} pages...",
            total=len(reader.pages)
        )

        for page_num, page in enumerate(reader.pages, 1):
            text = page.extract_text()
            if text.strip():
                pages.append(text)
            progress.update(task, advance=1)

    console.print(f"[green]✓ Extracted {len(pages)} pages[/green]")
    return pages


def chunk_pages(pages: list[str], chunk_size: int = 2000) -> list[str]:
    """Combine pages into chunks of approximately chunk_size characters"""
    chunks = []
    current_chunk = ""

    for page in pages:
        if len(current_chunk) + len(page) > chunk_size and current_chunk:
            chunks.append(current_chunk)
            current_chunk = page
        else:
            current_chunk += "\n\n" + page if current_chunk else page

    if current_chunk:
        chunks.append(current_chunk)

    return chunks


def process_book(book: BookConfig, azure_client: AzureAIClient, references_dir: Path):
    """Process a single book: extract PDF, convert to markdown"""
    console.print(f"\n[bold blue]Processing: {book.filename}[/bold blue]")
    console.print(f"Description: {book.description}")

    pdf_path = references_dir / book.filename
    if not pdf_path.exists():
        console.print(f"[red]✗ PDF not found: {pdf_path}[/red]")
        return

    # Create output directory
    output_dir = references_dir / "markdown" / book.output_name
    output_dir.mkdir(parents=True, exist_ok=True)

    # Extract text from PDF
    pages = extract_text_from_pdf(pdf_path)

    # Chunk pages for processing
    chunk_size = int(os.getenv("PDF_CHUNK_SIZE", "2000"))
    chunks = chunk_pages(pages, chunk_size)

    console.print(f"[cyan]Processing {len(chunks)} chunks through Azure AI...[/cyan]")

    # Process each chunk through Azure AI
    markdown_chunks = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task(
            "Converting to markdown...",
            total=len(chunks)
        )

        for i, chunk in enumerate(chunks, 1):
            try:
                markdown = azure_client.process_text_chunk(chunk)
                markdown_chunks.append(f"<!-- Chunk {i} -->\n\n{markdown}")
                progress.update(task, advance=1)
            except Exception as e:
                console.print(f"[yellow]Warning: Error processing chunk {i}: {e}[/yellow]")
                markdown_chunks.append(f"<!-- Chunk {i} - Error processing -->\n\n{chunk}")
                progress.update(task, advance=1)

    # Combine all markdown chunks
    full_markdown = "\n\n---\n\n".join(markdown_chunks)

    # Save to file
    output_file = output_dir / "full_content.md"
    output_file.write_text(full_markdown, encoding="utf-8")

    # Save metadata
    metadata = {
        "source_pdf": book.filename,
        "output_name": book.output_name,
        "description": book.description,
        "total_pages": len(pages),
        "total_chunks": len(chunks),
        "output_file": str(output_file)
    }
    metadata_file = output_dir / "metadata.json"
    metadata_file.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    console.print(f"[green]✓ Saved to {output_file}[/green]")
    console.print(f"[green]✓ Metadata saved to {metadata_file}[/green]")


def main():
    """Main entry point"""
    console.print("[bold magenta]PDF to Markdown Converter[/bold magenta]")
    console.print("Using Azure AI Foundry\n")

    # Get project root
    project_root = Path(__file__).parent.parent
    references_dir = project_root / "references"

    if not references_dir.exists():
        console.print(f"[red]Error: References directory not found at {references_dir}[/red]")
        sys.exit(1)

    # Initialize Azure AI client
    try:
        azure_client = AzureAIClient()
        azure_client.create_markdown_agent()
    except Exception as e:
        console.print(f"[red]Error initializing Azure AI: {e}[/red]")
        console.print("[yellow]Make sure you've set up .env.local with your Azure credentials[/yellow]")
        sys.exit(1)

    # Get books to process from command line or use defaults
    if len(sys.argv) > 1:
        book_names = sys.argv[1:]
        books_to_process = [
            book for book in PRIORITY_BOOKS
            if book.output_name in book_names or book.filename in book_names
        ]
        if not books_to_process:
            console.print(f"[red]No matching books found for: {book_names}[/red]")
            console.print("\nAvailable books:")
            for book in PRIORITY_BOOKS:
                console.print(f"  - {book.output_name} ({book.filename})")
            sys.exit(1)
    else:
        # Process priority 1 books by default
        books_to_process = [book for book in PRIORITY_BOOKS if book.priority == 1]

    console.print(f"[cyan]Processing {len(books_to_process)} book(s)...[/cyan]\n")

    # Process each book
    for book in books_to_process:
        try:
            process_book(book, azure_client, references_dir)
        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted by user[/yellow]")
            sys.exit(0)
        except Exception as e:
            console.print(f"[red]Error processing {book.filename}: {e}[/red]")
            continue

    console.print("\n[bold green]✓ Processing complete![/bold green]")
    console.print(f"Markdown files saved to: {references_dir / 'markdown'}")


if __name__ == "__main__":
    main()
