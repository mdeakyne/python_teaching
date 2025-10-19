# PDF-to-Skills Processing Scripts

These scripts automate the extraction of Python skills from reference PDFs using Azure AI Foundry.

## Overview

The workflow has three stages:

1. **PDF → Markdown** (`pdf_to_markdown.py`)
2. **Markdown → Skills** (`extract_skills.py`)
3. **Skills → Organized Tracks** (`organize_skills.py`)

## Setup

### 1. Configure Azure AI Foundry

Copy the environment template and fill in your credentials:

```bash
cp .env.local.template .env.local
```

Edit `.env.local` with your Azure AI Foundry credentials:
- Project connection string
- API endpoint and key
- Model deployment name

### 2. Install Dependencies

Dependencies are already installed via uv:
- `pypdf` - PDF text extraction
- `azure-ai-projects` - Azure AI Foundry client
- `azure-identity` - Azure authentication
- `pydantic` - Data validation
- `rich` - Beautiful CLI output
- `python-dotenv` - Environment variables

## Usage

### Step 1: Convert PDFs to Markdown

Convert priority books (or specify which ones):

```bash
# Convert default priority 1 books
uv run python scripts/pdf_to_markdown.py

# Convert specific books
uv run python scripts/pdf_to_markdown.py "dive-into-data-science" "beyond-basics-python"

# Or by filename
uv run python scripts/pdf_to_markdown.py "Dive Into Data Science.pdf"
```

**Output**: `references/markdown/{book-name}/full_content.md`

### Step 2: Extract Skills

Extract Python skills from the converted markdown:

```bash
uv run python scripts/extract_skills.py
```

This processes all markdown files in `references/markdown/` and uses Azure AI to identify discrete skills.

**Output**: `references/extracted/{book-name}_skills.json`

### Step 3: Organize & Map to Tracks

Map extracted skills to learning tracks and generate markdown files:

```bash
uv run python scripts/organize_skills.py
```

This:
- Deduplicates similar skills across books
- Uses Azure AI to map skills to tracks (data-science, web-development, automation, testing)
- Generates individual skill markdown files
- Creates master index and per-track indexes

**Output**:
- `skills/{track}/{skill-name}.md` - Individual skill files
- `skills/index.md` - Master catalog
- `skills/{track}/index.md` - Per-track indexes

## Directory Structure

```
references/              # Git-ignored
├── *.pdf               # Source PDFs (14 books)
├── markdown/           # Converted markdown
│   └── {book-name}/
│       ├── full_content.md
│       └── metadata.json
└── extracted/          # Extracted skills
    └── {book-name}_skills.json

skills/                 # Git-ignored
├── index.md           # Master catalog
├── data-science/      # Track-specific skills
│   ├── index.md
│   └── {skill}.md
├── web-development/
├── automation/
├── testing/
└── _metadata/
    └── organization_summary.json
```

## Priority Books

Books are processed based on priority:

**Priority 1** (default):
- Dive Into Data Science
- Beyond the Basics with Python

**Priority 2**:
- Book of Dash
- Impractical Python Projects

Add more books to `pdf_to_markdown.py::PRIORITY_BOOKS` as needed.

## Skill Format

Each skill markdown file contains:

```markdown
# Skill Name

**Tracks**: data-science, automation
**Difficulty**: intermediate
**Category**: Data Manipulation

## Description
Clear description of what learners will be able to do...

## Key Concepts
- Concept 1
- Concept 2

## Prerequisites
- [Other Skill](./other-skill.md)

## Related Skills
- [Related Skill](./related-skill.md)

## Learning Resources
- **Book Name**: Chapter X, Section Y
```

## Troubleshooting

### Azure AI Connection Issues

Make sure `.env.local` has:
- Valid `AZURE_PROJECT_CONNECTION_STRING`
- Correct `AZURE_AI_MODEL_DEPLOYMENT` name

### Processing Errors

- **PDF extraction fails**: Some PDFs may have protection or encoding issues
- **AI response parsing fails**: The scripts have fallbacks for malformed JSON
- **Rate limits**: Azure AI may have rate limits; add delays if needed

### Reprocessing

To reprocess a book:
- Delete the output file (e.g., `references/extracted/{book}_skills.json`)
- Run the script again

## Advanced Usage

### Custom Chunk Sizes

Adjust in `.env.local`:
```
PDF_CHUNK_SIZE=2000  # Characters per chunk
```

### Adding New Books

Edit `pdf_to_markdown.py` and add to `PRIORITY_BOOKS`:

```python
BookConfig(
    filename="New Book.pdf",
    output_name="new-book",
    priority=1,
    description="Book description"
)
```

## Next Steps

After generating skills:

1. Review skills in `skills/` directory
2. Use skills to inform lesson creation in `docs/{track}/lessons/`
3. Create exercises based on skill prerequisites
4. Build projects that combine multiple skills

The skills serve as a curriculum map for your training materials!
