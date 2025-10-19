#!/usr/bin/env python3
"""
Skill Extractor using Microsoft Agent Framework with Azure OpenAI

Reads markdown files from converted PDFs and uses Azure OpenAI agents to extract
discrete Python skills, concepts, and learning points.
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Optional

from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from azure.ai.agents import AgentsClient
from azure.core.credentials import AzureKeyCredential
from pydantic import BaseModel, Field


console = Console()


class Skill(BaseModel):
    """Represents a discrete Python skill or concept"""
    name: str = Field(description="Clear, concise skill name")
    description: str = Field(description="2-3 sentence description")
    category: str = Field(description="General category (e.g., Data Manipulation, Web APIs)")
    difficulty: str = Field(description="beginner, intermediate, or advanced")
    key_concepts: List[str] = Field(description="3-5 key concepts covered")
    source_book: str = Field(description="Book this skill came from")
    source_section: str = Field(description="Chapter or section reference")
    prerequisites: List[str] = Field(default_factory=list, description="Skills needed first")
    related_skills: List[str] = Field(default_factory=list, description="Related/similar skills")


class SkillExtraction(BaseModel):
    """Container for extracted skills from a book"""
    book_name: str
    skills: List[Skill]
    metadata: dict = Field(default_factory=dict)


class AzureOpenAISkillExtractor:
    """Wrapper for Azure OpenAI via Microsoft Agent Framework for skill extraction"""

    def __init__(self):
        load_dotenv(".env.local")

        self.api_key = os.getenv("AZURE_API_KEY")
        self.endpoint = os.getenv("AZURE_ENDPOINT")
        self.api_version = os.getenv("AZURE_API_VERSION", "2025-04-01-preview")
        self.deployment = os.getenv("AZURE_CHAT_DEPLOYMENT_NAME", "gpt-4o")

        if not self.api_key or not self.endpoint:
            console.print("[red]Error: AZURE_API_KEY and AZURE_ENDPOINT must be set in .env.local[/red]")
            sys.exit(1)

        try:
            self.client = AgentsClient(
                endpoint=self.endpoint,
                credential=AzureKeyCredential(self.api_key)
            )
        except Exception as e:
            console.print(f"[red]Error creating agent client: {e}[/red]")
            sys.exit(1)

        self.agent = None
        self.agent_id = None

    def create_skill_extraction_agent(self):
        """Create an agent specialized in extracting Python skills"""
        console.print("[cyan]Creating Azure OpenAI agent for skill extraction...[/cyan]")

        instructions = """You are an expert Python educator analyzing technical content to extract discrete, teachable skills.

Your task is to:
1. Read technical content about Python
2. Identify discrete skills that can be taught independently
3. For each skill, extract:
   - Clear, specific skill name (e.g., "Working with Pandas DataFrames")
   - 2-3 sentence description of what learners will be able to do
   - Category (Data Manipulation, Web Development, Testing, etc.)
   - Difficulty level (beginner, intermediate, advanced)
   - 3-5 key concepts covered by this skill
   - Chapter/section where this appears
   - Prerequisites (other skills needed first)
   - Related skills

Return ONLY a valid JSON array of skill objects following this structure:
[
  {
    "name": "Skill Name",
    "description": "What learners will be able to do...",
    "category": "Category Name",
    "difficulty": "intermediate",
    "key_concepts": ["concept1", "concept2"],
    "source_section": "Chapter 3: Section Name",
    "prerequisites": ["prerequisite skill"],
    "related_skills": ["related skill"]
  }
]

Be specific and practical. Focus on skills that can be taught and practiced."""

        try:
            self.agent = self.client.create_agent(
                model=self.deployment,
                name="python-skill-extractor",
                instructions=instructions
            )
            self.agent_id = self.agent.id
            console.print(f"[green]✓ Agent created: {self.agent_id} with model: {self.deployment}[/green]")
        except Exception as e:
            console.print(f"[red]Error creating agent: {e}[/red]")
            import traceback
            traceback.print_exc()
            sys.exit(1)

        return self.agent

    def extract_skills_from_content(self, content: str, book_name: str) -> List[Skill]:
        """Extract skills from markdown content"""
        try:
            prompt = f"Extract Python skills from this content:\n\n{content[:8000]}"  # Limit size

            # Create a thread and run the agent
            run = self.client.create_thread_and_run(
                agent_id=self.agent_id,
                thread={
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                }
            )

            # Get the messages from the thread
            messages = self.client.messages.list(thread_id=run.thread_id)

            # Extract the assistant's response
            response_text = None
            for message in messages.data:
                if message.role == "assistant":
                    if message.content and len(message.content) > 0:
                        text_content = message.content[0]
                        if hasattr(text_content, 'text'):
                            response_text = text_content.text.value
                            break

            if not response_text:
                return []

            # Try to parse JSON from response
            try:
                # Look for JSON array in the response
                start = response_text.find('[')
                end = response_text.rfind(']') + 1
                if start >= 0 and end > start:
                    json_text = response_text[start:end]
                    skills_data = json.loads(json_text)

                    # Convert to Skill objects
                    skills = []
                    for skill_dict in skills_data:
                        skill_dict['source_book'] = book_name
                        skills.append(Skill(**skill_dict))
                    return skills
            except json.JSONDecodeError as e:
                console.print(f"[yellow]Warning: Could not parse JSON response: {e}[/yellow]")
                console.print(f"Response: {response_text[:200]}...")

        except Exception as e:
            console.print(f"[yellow]Warning: Error extracting skills: {e}[/yellow]")

        return []


def process_markdown_file(
    markdown_path: Path,
    book_name: str,
    extractor: AzureOpenAISkillExtractor
) -> SkillExtraction:
    """Process a markdown file and extract skills"""
    console.print(f"\n[bold blue]Processing: {markdown_path.name}[/bold blue]")

    # Read the markdown content
    content = markdown_path.read_text(encoding="utf-8")

    # Split into chunks if too large
    chunk_size = int(os.getenv("PDF_CHUNK_SIZE", "8000"))
    chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]

    console.print(f"[cyan]Analyzing {len(chunks)} chunk(s) for skills...[/cyan]")

    # Extract skills from each chunk
    all_skills = []
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Extracting skills...", total=len(chunks))

        for chunk in chunks:
            try:
                skills = extractor.extract_skills_from_content(chunk, book_name)
                all_skills.extend(skills)
                progress.update(task, advance=1)
            except Exception as e:
                console.print(f"[yellow]Warning: Error extracting from chunk: {e}[/yellow]")
                progress.update(task, advance=1)

    console.print(f"[green]✓ Extracted {len(all_skills)} skills[/green]")

    # Create extraction result
    return SkillExtraction(
        book_name=book_name,
        skills=all_skills,
        metadata={
            "source_file": str(markdown_path),
            "total_chunks": len(chunks),
            "total_skills": len(all_skills)
        }
    )


def main():
    """Main entry point"""
    console.print("[bold magenta]Python Skill Extractor[/bold magenta]")
    console.print("Using Microsoft Agent Framework with Azure OpenAI\n")

    # Get project root
    project_root = Path(__file__).parent.parent
    markdown_dir = project_root / "references" / "markdown"
    extracted_dir = project_root / "references" / "extracted"

    extracted_dir.mkdir(parents=True, exist_ok=True)

    if not markdown_dir.exists():
        console.print(f"[red]Error: Markdown directory not found at {markdown_dir}[/red]")
        console.print("Run pdf_to_markdown.py first to convert PDFs")
        sys.exit(1)

    # Initialize Azure OpenAI client
    try:
        extractor = AzureOpenAISkillExtractor()
        extractor.create_skill_extraction_agent()
    except Exception as e:
        console.print(f"[red]Error initializing Azure OpenAI: {e}[/red]")
        sys.exit(1)

    # Find all markdown files to process
    markdown_files = list(markdown_dir.glob("*/full_content.md"))

    if not markdown_files:
        console.print(f"[yellow]No markdown files found in {markdown_dir}[/yellow]")
        console.print("Run pdf_to_markdown.py first")
        sys.exit(1)

    console.print(f"[cyan]Found {len(markdown_files)} book(s) to process[/cyan]\n")

    # Process each markdown file
    for md_file in markdown_files:
        book_name = md_file.parent.name

        # Check if already processed
        output_file = extracted_dir / f"{book_name}_skills.json"
        if output_file.exists():
            console.print(f"[yellow]Skipping {book_name} (already processed)[/yellow]")
            console.print(f"  Delete {output_file} to reprocess\n")
            continue

        try:
            # Extract skills
            extraction = process_markdown_file(md_file, book_name, extractor)

            # Save to JSON
            output_data = extraction.model_dump()
            output_file.write_text(json.dumps(output_data, indent=2), encoding="utf-8")

            console.print(f"[green]✓ Saved to {output_file}[/green]")

            # Print summary
            categories = {}
            for skill in extraction.skills:
                categories[skill.category] = categories.get(skill.category, 0) + 1

            console.print("\n[cyan]Skills by category:[/cyan]")
            for category, count in sorted(categories.items()):
                console.print(f"  {category}: {count}")
            console.print()

        except KeyboardInterrupt:
            console.print("\n[yellow]Interrupted by user[/yellow]")
            sys.exit(0)
        except Exception as e:
            console.print(f"[red]Error processing {book_name}: {e}[/red]")
            import traceback
            traceback.print_exc()
            continue

    console.print("\n[bold green]✓ Skill extraction complete![/bold green]")
    console.print(f"Skills saved to: {extracted_dir}")
    console.print("\nNext step: Run organize_skills.py to map skills to learning tracks")


if __name__ == "__main__":
    main()
