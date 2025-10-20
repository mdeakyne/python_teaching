# Agent Architecture - PDF-to-Skills Pipeline

This document describes the multi-agent architecture used to extract Python skills from PDF reference books using Microsoft Agent Framework.

## Table of Contents

1. [Overview](#overview)
2. [Architecture Pattern](#architecture-pattern)
3. [Agent Roles](#agent-roles)
4. [Workflow Orchestration](#workflow-orchestration)
5. [State Management](#state-management)
6. [Tool Functions](#tool-functions)
7. [Data Flow](#data-flow)
8. [Error Handling & Recovery](#error-handling--recovery)

---

## Overview

The PDF-to-Skills pipeline uses a **Magentic Orchestration Pattern** where specialized AI agents work collaboratively under the coordination of a workflow manager. This architecture provides:

- **Modularity**: Each agent has a specific responsibility
- **Scalability**: Agents can process multiple books in parallel
- **Reliability**: State persistence enables recovery from failures
- **Maintainability**: Clear separation of concerns
- **Extensibility**: Easy to add new agents or modify existing ones

### Technology Stack

- **Microsoft Agent Framework**: Core agent infrastructure
- **Azure OpenAI**: LLM provider for agent reasoning
- **Pydantic**: Data validation and modeling
- **asyncio**: Asynchronous execution
- **Rich**: Terminal UI and progress tracking

---

## Architecture Pattern

### Magentic Orchestration

The Magentic pattern consists of:

```
┌─────────────────────────────────────────────────┐
│           Workflow Orchestrator                 │
│  (SkillExtractionWorkflow)                     │
│                                                 │
│  - Manages overall pipeline                    │
│  - Coordinates specialist agents               │
│  - Handles state persistence                   │
│  - Tracks progress & checkpoints               │
└──────────────────┬──────────────────────────────┘
                   │
                   │ Delegates to Specialists
                   │
    ┌──────────────┴──────────────┐
    │                             │
    ▼                             ▼
┌─────────────┐              ┌─────────────┐
│  PDF        │              │  Skill      │
│  Extractor  │──────────────▶│ Identifier  │
│  Agent      │  Content     │  Agent      │
└─────────────┘              └──────┬──────┘
                                    │ Raw Skills
                                    │
                                    ▼
                             ┌─────────────┐
                             │  Validator  │
                             │  Agent      │
                             └──────┬──────┘
                                    │ Validated Skills
                                    │
                                    ▼
                             ┌─────────────┐
                             │ Categorizer │
                             │  Agent      │
                             └──────┬──────┘
                                    │ Organized Skills
                                    │
                                    ▼
                             ┌─────────────┐
                             │  Markdown   │
                             │  Generator  │
                             │  Agent      │
                             └─────────────┘
```

### Concurrent Processing

Multiple books can be processed simultaneously:

```
Book 1 ──┐
Book 2 ──┼──▶ [ PDF Extractor Agents ] ──▶ [ Skill Identifier Agents ]
Book 3 ──┘         (Parallel)                     (Parallel)
                                                        │
                                                        ▼
                                              [ Merge & Deduplicate ]
                                                        │
                                                        ▼
                                              [ Categorize & Validate ]
                                                        │
                                                        ▼
                                              [ Generate Markdown ]
```

---

## Agent Roles

### 1. PDF Extractor Agent

**Purpose**: Extract and structure content from PDF files

**Responsibilities**:
- Extract text from PDF pages
- Chunk content into processable segments
- Clean OCR artifacts and formatting
- Identify chapter/section boundaries
- Preserve code blocks and technical content

**Tools**:
- `extract_pdf_text(pdf_path)` - Extract text from PDF
- `chunk_content(content, chunk_size)` - Split into chunks

**Output**: Structured text content ready for analysis

---

### 2. Skill Identifier Agent

**Purpose**: Identify discrete, teachable Python skills from content

**Responsibilities**:
- Analyze technical content
- Identify atomic skills that can be taught independently
- Extract skill metadata (name, description, concepts, etc.)
- Ensure skills are well-defined and practical
- Validate skill structure

**Tools**:
- `validate_skill_structure(skill_json)` - Validate skill format
- `categorize_skill_content(description, concepts)` - Suggest category

**Output**: JSON array of extracted skills

**Skill Structure**:
```json
{
  "name": "Working with Pandas DataFrames",
  "description": "Learn to create, manipulate, and analyze data using Pandas DataFrames...",
  "category": "Data Manipulation",
  "difficulty": "intermediate",
  "key_concepts": ["DataFrame creation", "Column operations", "Filtering", "Grouping"],
  "source_section": "Chapter 3: Data Analysis",
  "prerequisites": ["Basic Python", "Understanding of tabular data"],
  "related_skills": ["NumPy Arrays", "Data Visualization"]
}
```

---

### 3. Validator Agent

**Purpose**: Ensure quality and completeness of extracted skills

**Responsibilities**:
- Validate skill structure and required fields
- Check for duplicate or similar skills
- Assess quality score
- Suggest improvements
- Merge similar skills when appropriate

**Tools**:
- `validate_skill_structure(skill_json)` - Structural validation
- `check_skill_similarity(name1, name2)` - Similarity detection
- `merge_skill_duplicates(skill1, skill2)` - Merge duplicates

**Quality Criteria**:
- All required fields present
- Clear, actionable descriptions
- Appropriate difficulty level
- Relevant key concepts
- No duplicates

---

### 4. Categorizer Agent

**Purpose**: Map skills to learning tracks

**Responsibilities**:
- Analyze skill content and concepts
- Assign to appropriate learning tracks
- Handle multi-track assignments
- Provide reasoning for categorization

**Learning Tracks**:
- **data-science**: Data analysis, ML, statistics, visualization
- **web-development**: APIs, web scraping, web frameworks
- **automation**: Scripting, CLI tools, task automation
- **testing**: Testing frameworks, TDD, code quality

**Tools**:
- `categorize_skill_content(description, concepts)` - Auto-categorization

**Output**: Skills with assigned tracks

---

### 5. Markdown Generator Agent

**Purpose**: Create formatted markdown documentation for skills

**Responsibilities**:
- Generate well-structured markdown files
- Create internal links between related skills
- Ensure consistent formatting
- Organize by learning tracks

**Tools**:
- `generate_skill_markdown(skill_json, tracks)` - Generate markdown
- `slugify(text)` - Create URL-friendly filenames

**Output Structure**:
```markdown
# Skill Name

**Tracks**: data-science, automation
**Difficulty**: intermediate
**Category**: Data Manipulation

## Description

[Clear description]

## Key Concepts

- Concept 1
- Concept 2

## Prerequisites

- [Related Skill](./related-skill.md)

## Learning Resources

- **Source Book**: Chapter reference

---

*Source: Book Name*
```

---

## Workflow Orchestration

### Workflow Manager (`SkillExtractionWorkflow`)

The workflow manager coordinates all agents and manages the pipeline:

**Key Responsibilities**:
1. Initialize agents with proper configuration
2. Manage workflow state and checkpointing
3. Coordinate sequential and parallel execution
4. Handle errors and retries
5. Track progress and report status
6. Aggregate results from multiple books

### Pipeline Stages

#### Stage 1: PDF Extraction
```python
for each book:
    PDFExtractorAgent.extract_content(pdf_path)
    → structured_content
```

#### Stage 2: Skill Identification
```python
for each content_chunk:
    SkillIdentifierAgent.identify_skills(chunk)
    → raw_skills[]
```

#### Stage 3: Validation
```python
for each skill:
    ValidatorAgent.validate(skill)
    if valid:
        validated_skills.append(skill)
```

#### Stage 4: Categorization
```python
for each skill:
    CategorizerAgent.assign_tracks(skill)
    → skill.tracks[]
```

#### Stage 5: Deduplication & Organization
```python
merged_skills = deduplicate(validated_skills)
organized_skills = organize_by_track(merged_skills)
```

#### Stage 6: Output Generation
```python
for each skill:
    MarkdownGeneratorAgent.generate(skill)
    save to output_dir/skills/{track}/{slug}.md
```

---

## State Management

### Checkpointing System

The pipeline implements robust state persistence:

**Checkpoint Triggers**:
- After each major stage completes
- After processing each book
- Before/after validation
- On manual save requests

**Checkpoint Contents**:
```json
{
  "workflow_id": "skill_extraction_20251019_143000",
  "workflow_name": "PDF to Skills Extraction",
  "created_at": "2025-10-19T14:30:00",
  "checkpoint_number": 15,
  "steps": [
    {
      "step_id": "extract_dive-into-data-science",
      "name": "Extract content from Dive Into Data Science.pdf",
      "status": "completed",
      "started_at": "2025-10-19T14:30:05",
      "completed_at": "2025-10-19T14:31:22",
      "result": {"content_length": 125430}
    }
  ],
  "global_state": {
    "total_books": 4,
    "completed_books": 2
  }
}
```

### Recovery Process

When resuming from a checkpoint:

1. Load workflow state from checkpoint file
2. Identify last completed step
3. Skip completed steps
4. Resume from next pending step
5. Continue normal execution

**Usage**:
```bash
# Original run (interrupted)
python scripts/agent_pipeline.py --books "Book1.pdf"

# Resume from checkpoint
python scripts/agent_pipeline.py --resume skill_extraction_20251019_143000
```

---

## Tool Functions

### Tool Registry

All agents have access to a shared pool of tools:

| Tool | Purpose | Used By |
|------|---------|---------|
| `extract_pdf_text` | Extract text from PDF | PDF Extractor |
| `chunk_content` | Split content into chunks | PDF Extractor |
| `validate_skill_structure` | Validate skill JSON | Skill Identifier, Validator |
| `check_skill_similarity` | Detect duplicates | Validator |
| `categorize_skill_content` | Auto-categorization | Skill Identifier, Categorizer |
| `generate_skill_markdown` | Create markdown files | Markdown Generator |
| `slugify` | Create URL slugs | Markdown Generator |
| `merge_skill_duplicates` | Merge similar skills | Validator |

### Tool Decorator Pattern

Tools are defined with type hints for automatic schema inference:

```python
def extract_pdf_text(
    pdf_path: Annotated[str, Field(description="Path to PDF file")]
) -> str:
    """
    Extract all text content from a PDF file.

    Args:
        pdf_path: Path to the PDF file

    Returns:
        Extracted text as a single string
    """
    # Implementation
```

Agents can invoke tools through the framework:
```python
result = await agent.run("Extract content from /path/to/book.pdf")
```

---

## Data Flow

### Complete Data Flow Diagram

```
┌─────────────┐
│  PDF Files  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────┐
│  PDF Extractor Agent    │
│  + extract_pdf_text     │
│  + chunk_content        │
└──────┬──────────────────┘
       │
       │ Raw Text Chunks
       │
       ▼
┌─────────────────────────┐
│  Skill Identifier Agent │
│  + validate_skill       │
│  + categorize_content   │
└──────┬──────────────────┘
       │
       │ Raw Skills (JSON)
       │
       ▼
┌─────────────────────────┐
│  Validator Agent        │
│  + validate_structure   │
│  + check_similarity     │
│  + merge_duplicates     │
└──────┬──────────────────┘
       │
       │ Validated Skills
       │
       ▼
┌─────────────────────────┐
│  Categorizer Agent      │
│  + categorize_skill     │
└──────┬──────────────────┘
       │
       │ Categorized Skills
       │
       ▼
┌─────────────────────────┐
│  Deduplication          │
│  (Merge similar skills) │
└──────┬──────────────────┘
       │
       │ Unique Skills
       │
       ▼
┌─────────────────────────┐
│  Markdown Generator     │
│  + generate_markdown    │
│  + slugify              │
└──────┬──────────────────┘
       │
       ▼
┌──────────────────────────┐
│  Output Files            │
│  skills/                 │
│  ├── data-science/       │
│  ├── web-development/    │
│  ├── automation/         │
│  └── testing/            │
└──────────────────────────┘
```

---

## Error Handling & Recovery

### Error Handling Strategy

**Levels of Error Handling**:

1. **Tool Level**: Individual tools handle their own errors
   ```python
   try:
       result = extract_pdf_text(path)
   except Exception as e:
       return f"Error: {str(e)}"
   ```

2. **Agent Level**: Agents handle tool failures gracefully
   ```python
   if "Error" in result:
       console.print(f"[yellow]Tool failed: {result}[/yellow]")
       # Try alternative approach or skip
   ```

3. **Workflow Level**: Workflow manages step failures
   ```python
   try:
       await process_book(book)
   except Exception as e:
       state_manager.fail_step(step_id, str(e))
       # Continue with next book or halt
   ```

4. **Pipeline Level**: Overall pipeline handles catastrophic failures
   ```python
   try:
       await workflow.run(books)
   except Exception as e:
       console.print(f"[red]Pipeline failed: {e}[/red]")
       console.print("Progress saved. Use --resume to continue")
   ```

### Recovery Scenarios

**Scenario 1: Agent Timeout**
- Checkpoint current state
- Log the failure
- Retry with smaller chunk size
- Continue with next item if retry fails

**Scenario 2: Invalid Skill Data**
- Log validation errors
- Skip invalid skill
- Continue processing
- Report at end

**Scenario 3: Network Interruption**
- Checkpoint before each network call
- Automatic retry with exponential backoff
- Resume from last checkpoint

**Scenario 4: User Interruption (Ctrl+C)**
- Gracefully save current state
- Create checkpoint
- Display resume command
- Exit cleanly

### Best Practices

1. **Always checkpoint before expensive operations**
2. **Log all errors with context**
3. **Provide clear recovery instructions**
4. **Never lose processed data**
5. **Make resume seamless**

---

## Configuration

### Environment Variables

Required in `.env.local`:

```bash
# Azure OpenAI Configuration
AZURE_API_KEY=your_api_key_here
AZURE_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_CHAT_DEPLOYMENT_NAME=gpt-4o
AZURE_API_VERSION=2025-04-01-preview

# Pipeline Configuration
PDF_CHUNK_SIZE=8000
MAX_CONCURRENT_AGENTS=5
CHECKPOINT_DIR=references/_checkpoints
```

### Agent Configuration

Centralized in `src/teaching_utils/agent_config.py`:

```python
config = AgentConfiguration()
config.chunk_size              # 8000 chars
config.max_concurrent_agents   # 5 agents
config.checkpoint_dir          # Path to checkpoints
```

---

## Usage Examples

### Basic Usage

```bash
# Process all priority 1 books
python scripts/agent_pipeline.py

# Process specific books
python scripts/agent_pipeline.py --books "Dive Into Data Science.pdf"

# Process up to priority 2
python scripts/agent_pipeline.py --priority 2
```

### Advanced Usage

```bash
# Resume from checkpoint
python scripts/agent_pipeline.py --resume skill_extraction_20251019_143000

# Disable checkpointing (not recommended)
python scripts/agent_pipeline.py --no-checkpoint

# Custom output directory
python scripts/agent_pipeline.py --output-dir ./custom_output

# List available agents
python scripts/agent_pipeline.py --list-agents

# Show configuration
python scripts/agent_pipeline.py --show-config
```

---

## Extension Points

### Adding New Agents

1. Define agent role in `src/teaching_utils/agents.py`:
```python
NEW_AGENT = AgentRole(
    name="NewAgent",
    role="Description",
    instructions="Detailed instructions...",
    tools=[tool1, tool2]
)
```

2. Add to workflow in `src/teaching_utils/workflows.py`:
```python
async def _new_step(self, input_data):
    async with self.config.create_agent(
        instructions=NEW_AGENT.instructions,
        name=NEW_AGENT.name,
        tools=NEW_AGENT.tools
    ) as agent:
        result = await agent.run(prompt)
        return result
```

### Adding New Tools

1. Define tool in `src/teaching_utils/agent_tools.py`:
```python
def new_tool(
    param: Annotated[str, Field(description="Description")]
) -> str:
    """Tool documentation"""
    # Implementation
    return result
```

2. Add to appropriate agent's tools list
3. Update agent instructions to mention the tool

### Customizing Workflow

Modify `SkillExtractionWorkflow` in `workflows.py`:
- Add new stages
- Change orchestration pattern
- Modify parallel/sequential execution
- Customize checkpoint behavior

---

## Performance Considerations

### Optimization Strategies

1. **Parallel Processing**: Process multiple books simultaneously
2. **Chunk Optimization**: Balance chunk size vs. API calls
3. **Agent Reuse**: Keep agents alive across multiple calls
4. **Caching**: Cache similar prompts/responses
5. **Batch Operations**: Group similar operations

### Resource Management

- **Memory**: Monitor for large PDF content
- **API Limits**: Respect rate limits
- **Tokens**: Optimize prompt sizes
- **Concurrency**: Limit parallel agents
- **Checkpoints**: Clean up old checkpoints regularly

---

## Troubleshooting

### Common Issues

**Issue**: "Agent timeout"
- **Solution**: Reduce chunk size or increase timeout

**Issue**: "No skills extracted"
- **Solution**: Check PDF quality, ensure readable text

**Issue**: "Checkpoint not found"
- **Solution**: Verify checkpoint directory, check workflow ID

**Issue**: "Invalid JSON from agent"
- **Solution**: Review agent instructions, add examples

**Issue**: "Too many duplicate skills"
- **Solution**: Tune similarity threshold, improve validation

---

## References

- [Microsoft Agent Framework Documentation](https://learn.microsoft.com/en-us/agent-framework/)
- [Azure OpenAI Service](https://learn.microsoft.com/en-us/azure/ai-services/openai/)
- [Project README](../README.md)
- [Skills Reference](../skills.md)

---

**Last Updated**: 2025-10-19
**Version**: 1.0
**Architecture**: Magentic Multi-Agent Orchestration with State Persistence
