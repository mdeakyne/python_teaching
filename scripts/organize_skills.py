#!/usr/bin/env python3
"""
Skill Organizer using Azure AI Foundry

Takes extracted skills from multiple books, maps them to learning tracks,
deduplicates similar skills, and generates individual skill markdown files.
"""

import os
import sys
import json
from pathlib import Path
from typing import List, Dict, Set
from collections import defaultdict

from dotenv import load_dotenv
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.table import Table
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential
from pydantic import BaseModel, Field


console = Console()


class Skill(BaseModel):
    """Represents a discrete Python skill"""
    name: str
    description: str
    category: str
    difficulty: str
    key_concepts: List[str]
    source_book: str
    source_section: str
    prerequisites: List[str] = Field(default_factory=list)
    related_skills: List[str] = Field(default_factory=list)


class OrganizedSkill(BaseModel):
    """Skill mapped to learning tracks with additional metadata"""
    skill: Skill
    tracks: List[str] = Field(description="Which tracks this skill belongs to")
    skill_id: str = Field(description="Unique identifier (slugified name)")
    merged_from: List[str] = Field(default_factory=list, description="Books this was merged from")


class TrackMapping(BaseModel):
    """Maps a skill to learning tracks"""
    skill_name: str
    tracks: List[str]
    reasoning: str


class AzureAITrackMapper:
    """Azure AI agent for mapping skills to tracks"""

    TRACKS = [
        "data-science",
        "web-development",
        "automation",
        "testing"
    ]

    def __init__(self):
        load_dotenv(".env.local")

        connection_string = os.getenv("AZURE_PROJECT_CONNECTION_STRING")
        if not connection_string:
            console.print("[red]Error: AZURE_PROJECT_CONNECTION_STRING not set[/red]")
            sys.exit(1)

        self.client = AIProjectClient.from_connection_string(
            credential=DefaultAzureCredential(),
            conn_str=connection_string
        )

        self.agent = None

    def create_mapping_agent(self):
        """Create agent for track mapping"""
        console.print("[cyan]Creating Azure AI agent for track mapping...[/cyan]")

        self.agent = self.client.agents.create_agent(
            model=os.getenv("AZURE_AI_MODEL_DEPLOYMENT", "gpt-4"),
            name="skill-track-mapper",
            instructions=f"""You are an expert Python curriculum designer mapping skills to learning tracks.

Available tracks:
- data-science: Data analysis, pandas, numpy, visualization, statistics
- web-development: APIs, HTTP, web scraping, FastAPI, web services
- automation: Scripting, file operations, CLI tools, task automation
- testing: pytest, TDD, code quality, debugging, testing practices

Your task:
1. Read a Python skill description
2. Determine which track(s) it belongs to (can be multiple)
3. Provide brief reasoning

Return ONLY a valid JSON object:
{{
  "skill_name": "Exact skill name from input",
  "tracks": ["track1", "track2"],
  "reasoning": "Why this skill fits these tracks"
}}

Map skills to the most relevant tracks. A skill can belong to multiple tracks if applicable."""
        )

        console.print(f"[green]✓ Agent created: {self.agent.id}[/green]")
        return self.agent

    def map_skill_to_tracks(self, skill: Skill) -> TrackMapping:
        """Map a single skill to tracks"""
        # Create thread
        thread = self.client.agents.create_thread()

        # Prepare skill info
        skill_info = f"""Skill: {skill.name}
Description: {skill.description}
Category: {skill.category}
Key Concepts: {', '.join(skill.key_concepts)}"""

        # Send for mapping
        message = self.client.agents.create_message(
            thread_id=thread.id,
            role="user",
            content=f"Map this skill to learning tracks:\n\n{skill_info}"
        )

        # Run agent
        run = self.client.agents.create_and_process_run(
            thread_id=thread.id,
            agent_id=self.agent.id
        )

        # Get response
        messages = self.client.agents.list_messages(thread_id=thread.id)

        for msg in messages:
            if msg.role == "assistant":
                if hasattr(msg, 'content') and len(msg.content) > 0:
                    response_text = msg.content[0].text.value

                    try:
                        # Parse JSON
                        start = response_text.find('{')
                        end = response_text.rfind('}') + 1
                        if start >= 0 and end > start:
                            json_text = response_text[start:end]
                            mapping_data = json.loads(json_text)
                            return TrackMapping(**mapping_data)
                    except json.JSONDecodeError as e:
                        console.print(f"[yellow]Warning: Could not parse mapping for {skill.name}[/yellow]")

        # Fallback: guess based on category
        return self._guess_tracks_from_category(skill)

    def _guess_tracks_from_category(self, skill: Skill) -> TrackMapping:
        """Fallback track mapping based on category"""
        category_lower = skill.category.lower()

        if any(word in category_lower for word in ['data', 'pandas', 'numpy', 'visualization', 'analysis']):
            tracks = ['data-science']
        elif any(word in category_lower for word in ['web', 'api', 'http', 'scraping']):
            tracks = ['web-development']
        elif any(word in category_lower for word in ['test', 'debug', 'quality', 'tdd']):
            tracks = ['testing']
        elif any(word in category_lower for word in ['automation', 'script', 'file', 'cli']):
            tracks = ['automation']
        else:
            tracks = ['automation']  # Default fallback

        return TrackMapping(
            skill_name=skill.name,
            tracks=tracks,
            reasoning=f"Mapped based on category: {skill.category}"
        )


def load_all_skills(extracted_dir: Path) -> List[Skill]:
    """Load all skills from extracted JSON files"""
    all_skills = []

    for json_file in extracted_dir.glob("*_skills.json"):
        console.print(f"[cyan]Loading skills from {json_file.name}...[/cyan]")

        data = json.loads(json_file.read_text(encoding="utf-8"))

        for skill_data in data.get("skills", []):
            all_skills.append(Skill(**skill_data))

    console.print(f"[green]✓ Loaded {len(all_skills)} total skills[/green]\n")
    return all_skills


def slugify(text: str) -> str:
    """Convert text to URL-friendly slug"""
    import re
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def deduplicate_skills(skills: List[Skill]) -> List[OrganizedSkill]:
    """Merge similar skills from different books"""
    # Group by skill name (case-insensitive)
    skill_groups = defaultdict(list)

    for skill in skills:
        key = skill.name.lower().strip()
        skill_groups[key].append(skill)

    # Merge duplicates
    organized = []

    for skill_name, skill_list in skill_groups.items():
        if len(skill_list) == 1:
            # No duplicates
            skill = skill_list[0]
            organized.append(OrganizedSkill(
                skill=skill,
                tracks=[],  # Will be filled later
                skill_id=slugify(skill.name),
                merged_from=[skill.source_book]
            ))
        else:
            # Merge multiple occurrences
            # Use the first one as base, merge key_concepts and sources
            base_skill = skill_list[0]
            all_concepts = set(base_skill.key_concepts)
            all_sources = [base_skill.source_book]

            for other_skill in skill_list[1:]:
                all_concepts.update(other_skill.key_concepts)
                all_sources.append(other_skill.source_book)

            base_skill.key_concepts = sorted(list(all_concepts))

            organized.append(OrganizedSkill(
                skill=base_skill,
                tracks=[],
                skill_id=slugify(base_skill.name),
                merged_from=all_sources
            ))

    console.print(f"[green]✓ Deduplicated to {len(organized)} unique skills[/green]\n")
    return organized


def map_skills_to_tracks(
    organized_skills: List[OrganizedSkill],
    mapper: AzureAITrackMapper
) -> List[OrganizedSkill]:
    """Map each skill to appropriate tracks"""
    console.print("[cyan]Mapping skills to learning tracks...[/cyan]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task("Mapping...", total=len(organized_skills))

        for org_skill in organized_skills:
            try:
                mapping = mapper.map_skill_to_tracks(org_skill.skill)
                org_skill.tracks = mapping.tracks
                progress.update(task, advance=1)
            except Exception as e:
                console.print(f"[yellow]Warning: Error mapping {org_skill.skill.name}: {e}[/yellow]")
                org_skill.tracks = ['automation']  # Fallback
                progress.update(task, advance=1)

    return organized_skills


def generate_skill_markdown(org_skill: OrganizedSkill, skills_dir: Path):
    """Generate markdown file for a skill"""
    # Create markdown content
    content = f"""# {org_skill.skill.name}

**Tracks**: {', '.join(org_skill.tracks)}
**Difficulty**: {org_skill.skill.difficulty}
**Category**: {org_skill.skill.category}

## Description

{org_skill.skill.description}

## Key Concepts

"""

    for concept in org_skill.skill.key_concepts:
        content += f"- {concept}\n"

    if org_skill.skill.prerequisites:
        content += "\n## Prerequisites\n\n"
        for prereq in org_skill.skill.prerequisites:
            prereq_slug = slugify(prereq)
            content += f"- [{prereq}](./{prereq_slug}.md)\n"

    if org_skill.skill.related_skills:
        content += "\n## Related Skills\n\n"
        for related in org_skill.skill.related_skills:
            related_slug = slugify(related)
            content += f"- [{related}](./{related_slug}.md)\n"

    content += "\n## Learning Resources\n\n"
    for source in org_skill.merged_from:
        content += f"- **{source}**: {org_skill.skill.source_section}\n"

    content += f"\n---\n\n*Sources: {', '.join(org_skill.merged_from)}*\n"

    # Save to appropriate track directories
    for track in org_skill.tracks:
        track_dir = skills_dir / track
        track_dir.mkdir(parents=True, exist_ok=True)

        skill_file = track_dir / f"{org_skill.skill_id}.md"
        skill_file.write_text(content, encoding="utf-8")


def generate_index(organized_skills: List[OrganizedSkill], skills_dir: Path):
    """Generate master index and track indexes"""
    # Master index
    content = "# Python Skills Catalog\n\n"
    content += "A comprehensive catalog of Python skills extracted from reference materials.\n\n"

    # Group by track
    by_track = defaultdict(list)
    for org_skill in organized_skills:
        for track in org_skill.tracks:
            by_track[track].append(org_skill)

    # Create track sections
    for track in sorted(by_track.keys()):
        track_name = track.replace('-', ' ').title()
        content += f"\n## {track_name}\n\n"

        skills = sorted(by_track[track], key=lambda s: (s.skill.difficulty, s.skill.name))

        for org_skill in skills:
            content += f"- [{org_skill.skill.name}](./{track}/{org_skill.skill_id}.md) "
            content += f"*({org_skill.skill.difficulty})*\n"

    # Save master index
    (skills_dir / "index.md").write_text(content, encoding="utf-8")

    # Create per-track indexes
    for track, skills in by_track.items():
        track_dir = skills_dir / track
        track_name = track.replace('-', ' ').title()

        track_content = f"# {track_name} Skills\n\n"

        # Group by difficulty
        by_difficulty = defaultdict(list)
        for org_skill in skills:
            by_difficulty[org_skill.skill.difficulty].append(org_skill)

        for difficulty in ['beginner', 'intermediate', 'advanced']:
            if difficulty in by_difficulty:
                track_content += f"\n## {difficulty.title()}\n\n"
                for org_skill in sorted(by_difficulty[difficulty], key=lambda s: s.skill.name):
                    track_content += f"- [{org_skill.skill.name}](./{org_skill.skill_id}.md)\n"

        (track_dir / "index.md").write_text(track_content, encoding="utf-8")


def main():
    """Main entry point"""
    console.print("[bold magenta]Skill Organizer & Track Mapper[/bold magenta]")
    console.print("Using Azure AI Foundry\n")

    # Setup paths
    project_root = Path(__file__).parent.parent
    extracted_dir = project_root / "references" / "extracted"
    skills_dir = project_root / "skills"
    metadata_dir = skills_dir / "_metadata"

    metadata_dir.mkdir(parents=True, exist_ok=True)

    if not extracted_dir.exists() or not list(extracted_dir.glob("*_skills.json")):
        console.print(f"[red]Error: No extracted skills found in {extracted_dir}[/red]")
        console.print("Run extract_skills.py first")
        sys.exit(1)

    # Load all skills
    all_skills = load_all_skills(extracted_dir)

    # Deduplicate
    organized_skills = deduplicate_skills(all_skills)

    # Initialize Azure AI mapper
    try:
        mapper = AzureAITrackMapper()
        mapper.create_mapping_agent()
    except Exception as e:
        console.print(f"[red]Error initializing Azure AI: {e}[/red]")
        sys.exit(1)

    # Map to tracks
    organized_skills = map_skills_to_tracks(organized_skills, mapper)

    # Generate markdown files
    console.print("\n[cyan]Generating skill markdown files...[/cyan]")
    for org_skill in organized_skills:
        generate_skill_markdown(org_skill, skills_dir)

    console.print(f"[green]✓ Generated {len(organized_skills)} skill files[/green]")

    # Generate indexes
    console.print("\n[cyan]Generating indexes...[/cyan]")
    generate_index(organized_skills, skills_dir)
    console.print("[green]✓ Generated master and track indexes[/green]")

    # Save metadata
    metadata = {
        "total_skills": len(organized_skills),
        "by_track": {},
        "by_difficulty": {}
    }

    for org_skill in organized_skills:
        for track in org_skill.tracks:
            metadata["by_track"][track] = metadata["by_track"].get(track, 0) + 1

        diff = org_skill.skill.difficulty
        metadata["by_difficulty"][diff] = metadata["by_difficulty"].get(diff, 0) + 1

    metadata_file = metadata_dir / "organization_summary.json"
    metadata_file.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    # Print summary table
    console.print("\n[bold green]✓ Organization complete![/bold green]\n")

    table = Table(title="Skills by Track")
    table.add_column("Track", style="cyan")
    table.add_column("Skills", justify="right", style="green")

    for track, count in sorted(metadata["by_track"].items()):
        track_name = track.replace('-', ' ').title()
        table.add_row(track_name, str(count))

    console.print(table)

    console.print(f"\nSkills saved to: {skills_dir}")
    console.print(f"View master catalog: {skills_dir / 'index.md'}")


if __name__ == "__main__":
    main()
