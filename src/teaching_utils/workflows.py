"""
Multi-Agent Workflow Orchestration for PDF-to-Skills Pipeline

Implements the magentic orchestration pattern where a coordinator agent
manages specialist agents to process PDFs and extract Python skills.
"""

import asyncio
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from pydantic import BaseModel, Field

from .agent_config import AgentConfiguration, get_config
from .state_manager import StateManager, WorkflowState, StepStatus
from .agents import (
    PDF_EXTRACTOR_AGENT,
    SKILL_IDENTIFIER_AGENT,
    CATEGORIZER_AGENT,
    VALIDATOR_AGENT,
    MARKDOWN_GENERATOR_AGENT
)


console = Console()


class BookToProcess(BaseModel):
    """Represents a book to process"""
    filename: str
    output_name: str
    priority: int = 0
    description: str = ""
    pdf_path: Optional[Path] = None


class ExtractedSkill(BaseModel):
    """Represents an extracted skill"""
    name: str
    description: str
    category: str
    difficulty: str
    key_concepts: List[str]
    source_book: str
    source_section: str
    prerequisites: List[str] = Field(default_factory=list)
    related_skills: List[str] = Field(default_factory=list)
    tracks: List[str] = Field(default_factory=list)
    validation_score: Optional[float] = None


class SkillExtractionWorkflow:
    """
    Multi-agent workflow for extracting Python skills from PDF books.

    Uses the Magentic orchestration pattern where specialist agents work
    in parallel coordinated by a workflow manager.
    """

    def __init__(
        self,
        config: Optional[AgentConfiguration] = None,
        checkpoint_dir: Optional[Path] = None
    ):
        """
        Initialize the workflow.

        Args:
            config: Agent configuration (uses global if None)
            checkpoint_dir: Directory for checkpoints (uses config default if None)
        """
        self.config = config or get_config()
        self.state_manager = StateManager(
            checkpoint_dir or self.config.checkpoint_dir
        )
        self.workflow_state: Optional[WorkflowState] = None

    async def run(
        self,
        books: List[BookToProcess],
        references_dir: Path,
        output_dir: Path,
        workflow_id: Optional[str] = None,
        resume: bool = True
    ) -> Dict[str, Any]:
        """
        Run the complete skill extraction workflow.

        Args:
            books: List of books to process
            references_dir: Directory containing PDF files
            output_dir: Directory for output files
            workflow_id: Optional workflow ID (generated if None)
            resume: Whether to resume from checkpoint if available

        Returns:
            Dictionary with workflow results
        """
        # Generate workflow ID if not provided
        if workflow_id is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            workflow_id = f"skill_extraction_{timestamp}"

        # Try to resume from checkpoint
        if resume:
            self.workflow_state = self.state_manager.load_workflow(workflow_id)

        # Create new workflow if not resuming or no checkpoint found
        if self.workflow_state is None:
            console.print("[bold cyan]Starting new workflow...[/bold cyan]")
            step_names = self._generate_step_names(books)
            self.workflow_state = self.state_manager.create_workflow(
                workflow_id=workflow_id,
                workflow_name="PDF to Skills Extraction",
                step_names=step_names
            )
        else:
            console.print("[bold yellow]Resuming from checkpoint...[/bold yellow]")
            self.state_manager.print_workflow_status(self.workflow_state)

        # Process each book
        all_skills = []

        for book in books:
            try:
                book.pdf_path = references_dir / book.filename

                if not book.pdf_path.exists():
                    console.print(f"[red]PDF not found: {book.pdf_path}[/red]")
                    continue

                skills = await self._process_single_book(book, output_dir)
                all_skills.extend(skills)

            except Exception as e:
                console.print(f"[red]Error processing {book.filename}: {e}[/red]")
                import traceback
                traceback.print_exc()
                continue

        # Deduplicate and organize skills
        organized_skills = await self._organize_skills(all_skills, output_dir)

        # Generate final outputs
        await self._generate_outputs(organized_skills, output_dir)

        # Mark workflow complete
        console.print("\n[bold green]✓ Workflow completed successfully![/bold green]")
        self.state_manager.print_workflow_status(self.workflow_state)

        return {
            "workflow_id": workflow_id,
            "total_books": len(books),
            "total_skills": len(organized_skills),
            "output_dir": str(output_dir)
        }

    async def _process_single_book(
        self,
        book: BookToProcess,
        output_dir: Path
    ) -> List[ExtractedSkill]:
        """
        Process a single book through the multi-agent pipeline.

        Args:
            book: Book to process
            output_dir: Output directory

        Returns:
            List of extracted skills
        """
        console.print(f"\n[bold blue]Processing: {book.filename}[/bold blue]")

        # Step 1: Extract PDF content
        step_id = f"extract_{book.output_name}"
        if not self._is_step_complete(step_id):
            self.state_manager.start_step(self.workflow_state, step_id)

            try:
                content = await self._extract_pdf_content(book)
                self.state_manager.complete_step(
                    self.workflow_state,
                    step_id,
                    {"content_length": len(content)}
                )
            except Exception as e:
                self.state_manager.fail_step(self.workflow_state, step_id, str(e))
                raise

        # Step 2: Identify skills
        step_id = f"identify_{book.output_name}"
        if not self._is_step_complete(step_id):
            self.state_manager.start_step(self.workflow_state, step_id)

            try:
                raw_skills = await self._identify_skills(book, content)
                self.state_manager.complete_step(
                    self.workflow_state,
                    step_id,
                    {"skills_found": len(raw_skills)}
                )
            except Exception as e:
                self.state_manager.fail_step(self.workflow_state, step_id, str(e))
                raise

        # Step 3: Validate skills
        step_id = f"validate_{book.output_name}"
        if not self._is_step_complete(step_id):
            self.state_manager.start_step(self.workflow_state, step_id)

            try:
                validated_skills = await self._validate_skills(raw_skills)
                self.state_manager.complete_step(
                    self.workflow_state,
                    step_id,
                    {"valid_skills": len(validated_skills)}
                )
            except Exception as e:
                self.state_manager.fail_step(self.workflow_state, step_id, str(e))
                raise

        # Step 4: Categorize skills
        step_id = f"categorize_{book.output_name}"
        if not self._is_step_complete(step_id):
            self.state_manager.start_step(self.workflow_state, step_id)

            try:
                categorized_skills = await self._categorize_skills(validated_skills)
                self.state_manager.complete_step(
                    self.workflow_state,
                    step_id,
                    {"categorized_skills": len(categorized_skills)}
                )
            except Exception as e:
                self.state_manager.fail_step(self.workflow_state, step_id, str(e))
                raise

        return categorized_skills

    async def _extract_pdf_content(self, book: BookToProcess) -> str:
        """
        Extract content from PDF using PDFExtractorAgent.

        Args:
            book: Book to process

        Returns:
            Extracted and structured content
        """
        console.print(f"[cyan]Extracting content from {book.filename}...[/cyan]")

        async with self.config.create_agent(
            instructions=PDF_EXTRACTOR_AGENT.instructions,
            name=PDF_EXTRACTOR_AGENT.name,
            tools=PDF_EXTRACTOR_AGENT.tools
        ) as agent:
            # Ask agent to extract PDF content
            prompt = f"Extract all content from the PDF at: {book.pdf_path}"
            response = await agent.run(prompt)

            # For now, directly extract (in real implementation, use tools)
            from pypdf import PdfReader
            reader = PdfReader(book.pdf_path)
            content = "\n\n".join(
                page.extract_text()
                for page in reader.pages
                if page.extract_text().strip()
            )

            console.print(f"[green]✓ Extracted {len(content)} characters[/green]")
            return content

    async def _identify_skills(
        self,
        book: BookToProcess,
        content: str
    ) -> List[ExtractedSkill]:
        """
        Identify skills from content using SkillIdentifierAgent.

        Args:
            book: Book being processed
            content: Extracted content

        Returns:
            List of identified skills
        """
        console.print(f"[cyan]Identifying skills in {book.filename}...[/cyan]")

        # Chunk content for processing
        from .agent_tools import chunk_content
        chunks = chunk_content(content, self.config.chunk_size)

        all_skills = []

        # Process chunks with progress bar
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            console=console
        ) as progress:
            task = progress.add_task(
                f"Processing {len(chunks)} chunks...",
                total=len(chunks)
            )

            # Create agent for skill identification
            async with self.config.create_agent(
                instructions=SKILL_IDENTIFIER_AGENT.instructions,
                name=SKILL_IDENTIFIER_AGENT.name,
                tools=SKILL_IDENTIFIER_AGENT.tools
            ) as agent:

                # Process chunks (can be parallelized)
                for chunk in chunks:
                    try:
                        prompt = f"""Extract Python skills from this content.
Source book: {book.filename}

Content:
{chunk[:6000]}

Return a JSON array of skills."""

                        response = await agent.run(prompt)

                        # Parse response for skills
                        # Try to extract JSON array from response
                        response_text = str(response)
                        start = response_text.find('[')
                        end = response_text.rfind(']') + 1

                        if start >= 0 and end > start:
                            skills_data = json.loads(response_text[start:end])

                            for skill_dict in skills_data:
                                skill_dict['source_book'] = book.output_name
                                all_skills.append(ExtractedSkill(**skill_dict))

                    except Exception as e:
                        console.print(f"[yellow]Warning: Error processing chunk: {e}[/yellow]")

                    progress.update(task, advance=1)

        console.print(f"[green]✓ Identified {len(all_skills)} skills[/green]")
        return all_skills

    async def _validate_skills(
        self,
        skills: List[ExtractedSkill]
    ) -> List[ExtractedSkill]:
        """
        Validate skills using ValidatorAgent.

        Args:
            skills: Skills to validate

        Returns:
            List of validated skills
        """
        console.print(f"[cyan]Validating {len(skills)} skills...[/cyan]")

        validated = []

        async with self.config.create_agent(
            instructions=VALIDATOR_AGENT.instructions,
            name=VALIDATOR_AGENT.name,
            tools=VALIDATOR_AGENT.tools
        ) as agent:

            for skill in skills:
                try:
                    # Validate skill structure
                    skill_json = skill.model_dump_json()

                    from .agent_tools import validate_skill_structure
                    result = validate_skill_structure(skill_json)

                    if result['is_valid']:
                        validated.append(skill)
                    else:
                        console.print(f"[yellow]Skipping invalid skill: {skill.name}[/yellow]")
                        for error in result['errors']:
                            console.print(f"  - {error}")

                except Exception as e:
                    console.print(f"[yellow]Error validating {skill.name}: {e}[/yellow]")

        console.print(f"[green]✓ Validated {len(validated)} skills[/green]")
        return validated

    async def _categorize_skills(
        self,
        skills: List[ExtractedSkill]
    ) -> List[ExtractedSkill]:
        """
        Categorize skills and assign to tracks using CategorizerAgent.

        Args:
            skills: Skills to categorize

        Returns:
            List of categorized skills
        """
        console.print(f"[cyan]Categorizing {len(skills)} skills...[/cyan]")

        async with self.config.create_agent(
            instructions=CATEGORIZER_AGENT.instructions,
            name=CATEGORIZER_AGENT.name,
            tools=CATEGORIZER_AGENT.tools
        ) as agent:

            for skill in skills:
                try:
                    # Ask agent to categorize
                    prompt = f"""Map this skill to learning tracks:

Skill: {skill.name}
Description: {skill.description}
Category: {skill.category}
Key Concepts: {', '.join(skill.key_concepts)}

Return JSON with tracks array."""

                    response = await agent.run(prompt)
                    response_text = str(response)

                    # Try to parse tracks from response
                    start = response_text.find('{')
                    end = response_text.rfind('}') + 1

                    if start >= 0 and end > start:
                        mapping = json.loads(response_text[start:end])
                        skill.tracks = mapping.get('tracks', ['automation'])
                    else:
                        # Fallback categorization
                        from .agent_tools import categorize_skill_content
                        category = categorize_skill_content(
                            skill.description,
                            skill.key_concepts
                        )
                        skill.tracks = [self._category_to_track(category)]

                except Exception as e:
                    console.print(f"[yellow]Error categorizing {skill.name}: {e}[/yellow]")
                    skill.tracks = ['automation']  # Default fallback

        console.print(f"[green]✓ Categorized {len(skills)} skills[/green]")
        return skills

    async def _organize_skills(
        self,
        skills: List[ExtractedSkill],
        output_dir: Path
    ) -> List[ExtractedSkill]:
        """
        Deduplicate and organize skills.

        Args:
            skills: All extracted skills
            output_dir: Output directory

        Returns:
            Organized skills
        """
        console.print(f"\n[cyan]Organizing {len(skills)} skills...[/cyan]")

        # Simple deduplication by name
        unique_skills = {}
        for skill in skills:
            key = skill.name.lower().strip()

            if key not in unique_skills:
                unique_skills[key] = skill
            else:
                # Merge key concepts
                existing = unique_skills[key]
                existing.key_concepts = list(set(
                    existing.key_concepts + skill.key_concepts
                ))

        organized = list(unique_skills.values())
        console.print(f"[green]✓ Organized into {len(organized)} unique skills[/green]")

        return organized

    async def _generate_outputs(
        self,
        skills: List[ExtractedSkill],
        output_dir: Path
    ):
        """
        Generate markdown files and indexes.

        Args:
            skills: Organized skills
            output_dir: Output directory
        """
        console.print(f"\n[cyan]Generating output files...[/cyan]")

        skills_dir = output_dir / "skills"
        skills_dir.mkdir(parents=True, exist_ok=True)

        # Generate individual skill files
        from .agent_tools import generate_skill_markdown, slugify

        for skill in skills:
            skill_json = skill.model_dump_json()
            markdown = generate_skill_markdown(skill_json, skill.tracks)

            # Save to each track directory
            for track in skill.tracks:
                track_dir = skills_dir / track
                track_dir.mkdir(parents=True, exist_ok=True)

                skill_file = track_dir / f"{slugify(skill.name)}.md"
                skill_file.write_text(markdown, encoding="utf-8")

        console.print(f"[green]✓ Generated {len(skills)} skill files[/green]")

    def _generate_step_names(self, books: List[BookToProcess]) -> List[str]:
        """Generate step names for all books"""
        steps = []
        for book in books:
            steps.extend([
                f"extract_{book.output_name}",
                f"identify_{book.output_name}",
                f"validate_{book.output_name}",
                f"categorize_{book.output_name}"
            ])
        steps.append("organize_all")
        steps.append("generate_outputs")
        return steps

    def _is_step_complete(self, step_id: str) -> bool:
        """Check if a step is already complete"""
        step = self.state_manager.get_step(self.workflow_state, step_id)
        return step and step.status == StepStatus.COMPLETED

    @staticmethod
    def _category_to_track(category: str) -> str:
        """Map category to track"""
        category_lower = category.lower()

        if 'data' in category_lower or 'analysis' in category_lower:
            return 'data-science'
        elif 'web' in category_lower or 'api' in category_lower:
            return 'web-development'
        elif 'test' in category_lower:
            return 'testing'
        elif any(word in category_lower for word in ['clean', 'pattern', 'refactor', 'solid', 'design', 'architect', 'structure']):
            return 'clean-code'
        else:
            return 'automation'
