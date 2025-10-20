"""
Workflow State Management with Checkpointing

Provides state persistence and recovery for long-running agent workflows,
enabling resumption from failures and tracking pipeline progress.
"""

import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field
from rich.console import Console


console = Console()


class StepStatus(str, Enum):
    """Status of a workflow step"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class WorkflowStep(BaseModel):
    """Represents a single step in the workflow"""
    step_id: str = Field(description="Unique identifier for this step")
    name: str = Field(description="Human-readable step name")
    status: StepStatus = Field(default=StepStatus.PENDING)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any] = Field(default_factory=dict)


class WorkflowState(BaseModel):
    """Complete state of a workflow with checkpointing"""
    workflow_id: str = Field(description="Unique workflow identifier")
    workflow_name: str = Field(description="Human-readable workflow name")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    checkpoint_number: int = Field(default=0)
    steps: List[WorkflowStep] = Field(default_factory=list)
    global_state: Dict[str, Any] = Field(
        default_factory=dict,
        description="Shared state across all steps"
    )
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


class StateManager:
    """Manages workflow state with checkpoint persistence"""

    def __init__(self, checkpoint_dir: Path):
        """
        Initialize state manager.

        Args:
            checkpoint_dir: Directory for storing checkpoint files
        """
        self.checkpoint_dir = Path(checkpoint_dir)
        self.checkpoint_dir.mkdir(parents=True, exist_ok=True)

    def create_workflow(
        self,
        workflow_id: str,
        workflow_name: str,
        step_names: List[str]
    ) -> WorkflowState:
        """
        Create a new workflow with defined steps.

        Args:
            workflow_id: Unique identifier
            workflow_name: Descriptive name
            step_names: List of step names to create

        Returns:
            New WorkflowState instance
        """
        steps = [
            WorkflowStep(
                step_id=name,  # Use step name directly as ID
                name=name
            )
            for i, name in enumerate(step_names, 1)
        ]

        state = WorkflowState(
            workflow_id=workflow_id,
            workflow_name=workflow_name,
            steps=steps
        )

        # Save initial checkpoint
        self.save_checkpoint(state)
        console.print(f"[green]✓ Created workflow: {workflow_name} ({workflow_id})[/green]")

        return state

    def load_workflow(self, workflow_id: str) -> Optional[WorkflowState]:
        """
        Load workflow state from checkpoint.

        Args:
            workflow_id: Workflow identifier

        Returns:
            WorkflowState if found, None otherwise
        """
        checkpoint_path = self._get_checkpoint_path(workflow_id)

        if not checkpoint_path.exists():
            console.print(f"[yellow]No checkpoint found for: {workflow_id}[/yellow]")
            return None

        try:
            data = json.loads(checkpoint_path.read_text(encoding="utf-8"))
            state = WorkflowState(**data)
            console.print(f"[cyan]Loaded checkpoint #{state.checkpoint_number} for: {workflow_id}[/cyan]")
            return state
        except Exception as e:
            console.print(f"[red]Error loading checkpoint: {e}[/red]")
            return None

    def save_checkpoint(self, state: WorkflowState) -> Path:
        """
        Save workflow state to checkpoint file.

        Args:
            state: Current workflow state

        Returns:
            Path to saved checkpoint file
        """
        state.updated_at = datetime.now()
        state.checkpoint_number += 1

        checkpoint_path = self._get_checkpoint_path(state.workflow_id)

        try:
            # Save as JSON
            data = state.model_dump(mode='json')
            checkpoint_path.write_text(
                json.dumps(data, indent=2, default=str),
                encoding="utf-8"
            )

            # Also save a numbered backup
            backup_path = self._get_checkpoint_path(
                state.workflow_id,
                checkpoint_num=state.checkpoint_number
            )
            backup_path.write_text(
                json.dumps(data, indent=2, default=str),
                encoding="utf-8"
            )

            console.print(f"[dim]Checkpoint #{state.checkpoint_number} saved[/dim]")
            return checkpoint_path

        except Exception as e:
            console.print(f"[red]Error saving checkpoint: {e}[/red]")
            raise

    def get_step(self, state: WorkflowState, step_id: str) -> Optional[WorkflowStep]:
        """Get a specific step by ID"""
        for step in state.steps:
            if step.step_id == step_id:
                return step
        return None

    def get_step_by_name(self, state: WorkflowState, step_name: str) -> Optional[WorkflowStep]:
        """Get a specific step by name"""
        for step in state.steps:
            if step.name == step_name:
                return step
        return None

    def start_step(
        self,
        state: WorkflowState,
        step_id: str,
        save: bool = True
    ) -> WorkflowStep:
        """
        Mark a step as started.

        Args:
            state: Workflow state
            step_id: Step identifier
            save: Whether to save checkpoint immediately

        Returns:
            Updated WorkflowStep
        """
        step = self.get_step(state, step_id)
        if not step:
            raise ValueError(f"Step not found: {step_id}")

        step.status = StepStatus.IN_PROGRESS
        step.started_at = datetime.now()

        console.print(f"[cyan]→ Starting: {step.name}[/cyan]")

        if save:
            self.save_checkpoint(state)

        return step

    def complete_step(
        self,
        state: WorkflowState,
        step_id: str,
        result: Optional[Dict[str, Any]] = None,
        save: bool = True
    ) -> WorkflowStep:
        """
        Mark a step as completed.

        Args:
            state: Workflow state
            step_id: Step identifier
            result: Optional result data
            save: Whether to save checkpoint immediately

        Returns:
            Updated WorkflowStep
        """
        step = self.get_step(state, step_id)
        if not step:
            raise ValueError(f"Step not found: {step_id}")

        step.status = StepStatus.COMPLETED
        step.completed_at = datetime.now()
        if result:
            step.result = result

        duration = ""
        if step.started_at:
            delta = step.completed_at - step.started_at
            duration = f" ({delta.total_seconds():.1f}s)"

        console.print(f"[green]✓ Completed: {step.name}{duration}[/green]")

        if save:
            self.save_checkpoint(state)

        return step

    def fail_step(
        self,
        state: WorkflowState,
        step_id: str,
        error: str,
        save: bool = True
    ) -> WorkflowStep:
        """
        Mark a step as failed.

        Args:
            state: Workflow state
            step_id: Step identifier
            error: Error message
            save: Whether to save checkpoint immediately

        Returns:
            Updated WorkflowStep
        """
        step = self.get_step(state, step_id)
        if not step:
            raise ValueError(f"Step not found: {step_id}")

        step.status = StepStatus.FAILED
        step.completed_at = datetime.now()
        step.error_message = error

        console.print(f"[red]✗ Failed: {step.name}[/red]")
        console.print(f"[red]  Error: {error}[/red]")

        if save:
            self.save_checkpoint(state)

        return step

    def get_next_pending_step(self, state: WorkflowState) -> Optional[WorkflowStep]:
        """
        Get the next pending step to execute.

        Returns:
            Next pending WorkflowStep or None if all complete
        """
        for step in state.steps:
            if step.status == StepStatus.PENDING:
                return step
        return None

    def is_workflow_complete(self, state: WorkflowState) -> bool:
        """Check if all steps are completed"""
        return all(
            step.status in (StepStatus.COMPLETED, StepStatus.SKIPPED)
            for step in state.steps
        )

    def get_workflow_summary(self, state: WorkflowState) -> Dict[str, int]:
        """Get summary statistics of workflow state"""
        summary = {
            "total_steps": len(state.steps),
            "pending": 0,
            "in_progress": 0,
            "completed": 0,
            "failed": 0,
            "skipped": 0
        }

        for step in state.steps:
            if step.status == StepStatus.PENDING:
                summary["pending"] += 1
            elif step.status == StepStatus.IN_PROGRESS:
                summary["in_progress"] += 1
            elif step.status == StepStatus.COMPLETED:
                summary["completed"] += 1
            elif step.status == StepStatus.FAILED:
                summary["failed"] += 1
            elif step.status == StepStatus.SKIPPED:
                summary["skipped"] += 1

        return summary

    def print_workflow_status(self, state: WorkflowState):
        """Print current workflow status to console"""
        console.print(f"\n[bold]Workflow: {state.workflow_name}[/bold]")
        console.print(f"ID: {state.workflow_id}")
        console.print(f"Checkpoint: #{state.checkpoint_number}")

        summary = self.get_workflow_summary(state)
        console.print(f"\nProgress: {summary['completed']}/{summary['total_steps']} steps completed")

        if summary['failed'] > 0:
            console.print(f"[red]Failed: {summary['failed']}[/red]")
        if summary['in_progress'] > 0:
            console.print(f"[cyan]In Progress: {summary['in_progress']}[/cyan]")
        if summary['pending'] > 0:
            console.print(f"[yellow]Pending: {summary['pending']}[/yellow]")

        console.print("\nSteps:")
        for step in state.steps:
            status_icon = {
                StepStatus.COMPLETED: "✓",
                StepStatus.FAILED: "✗",
                StepStatus.IN_PROGRESS: "→",
                StepStatus.PENDING: "○",
                StepStatus.SKIPPED: "⊘"
            }.get(step.status, "?")

            status_color = {
                StepStatus.COMPLETED: "green",
                StepStatus.FAILED: "red",
                StepStatus.IN_PROGRESS: "cyan",
                StepStatus.PENDING: "yellow",
                StepStatus.SKIPPED: "dim"
            }.get(step.status, "white")

            console.print(f"  [{status_color}]{status_icon} {step.name}[/{status_color}]")

    def _get_checkpoint_path(
        self,
        workflow_id: str,
        checkpoint_num: Optional[int] = None
    ) -> Path:
        """Get path to checkpoint file"""
        if checkpoint_num is None:
            filename = f"{workflow_id}.json"
        else:
            filename = f"{workflow_id}_checkpoint_{checkpoint_num:04d}.json"

        return self.checkpoint_dir / filename

    @staticmethod
    def _slugify(text: str) -> str:
        """Convert text to slug"""
        import re
        text = text.lower()
        text = re.sub(r'[^\w\s-]', '', text)
        text = re.sub(r'[-\s]+', '-', text)
        return text.strip('-')

    def cleanup_old_checkpoints(
        self,
        workflow_id: str,
        keep_last: int = 10
    ):
        """
        Remove old checkpoint backups, keeping only the most recent.

        Args:
            workflow_id: Workflow identifier
            keep_last: Number of recent checkpoints to keep
        """
        pattern = f"{workflow_id}_checkpoint_*.json"
        checkpoints = sorted(
            self.checkpoint_dir.glob(pattern),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )

        for checkpoint in checkpoints[keep_last:]:
            checkpoint.unlink()
            console.print(f"[dim]Removed old checkpoint: {checkpoint.name}[/dim]")
