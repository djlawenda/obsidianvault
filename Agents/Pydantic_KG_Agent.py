import os
import re
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

from pydantic_ai import Agent, RunContext
from pydantic_ai.models.google import GoogleModel

from Models import KnowledgeExtraction, HubNode, ConceptNode, TechNode

# --- Constants and Configuration ---

VAULT_ROOT = Path("/home/lukasz/Documents/ObsidianVault")
AGENT_DIR = VAULT_ROOT / "Agents"
INBOX_DIR = VAULT_ROOT / "Inbox"
RESOURCES_DIR = VAULT_ROOT / "Resources"
PROCESSED_TRANSCRIPTS_DIR = RESOURCES_DIR / "Processed_Transcripts"
HUBS_DIR = RESOURCES_DIR / "Hubs"
CONCEPTS_DIR = RESOURCES_DIR / "Concepts"
TECH_DIR = RESOURCES_DIR / "Technologies"

HUB_TEMPLATE = """---
type: "Hub"
tags: [hub, {tag}]
---
# {title}

{description}

## Concepts
- 

## Excerpts & Key Information

## Further Reading

> Core Node: [[Projects/Second_Brain]]
"""

CONCEPT_TEMPLATE = """---
type: "Concept"
hub: "{hub}"
tags: [concept, {tag}]
---
# {title}

{description}

## Technologies
- 

## Excerpts & Key Information

## Further Reading

> Core Node: [[Projects/Second_Brain]]
"""

TECHNOLOGY_TEMPLATE = """---
type: "Technology"
concept: "{concept}"
tags: [technology, {tag}]
---
# {title}

{description}

## Excerpts & Key Information

## Further Reading

### Source
*   Original reference: {source}

> Core Node: [[Projects/Second_Brain]]
"""

def sanitize_filename(name: str) -> str:
    name = name.title()
    name = re.sub(r'[ -]', '_', name)
    name = re.sub(r'[^a-zA-Z0-9_]', '', name)
    return name

# --- Pydantic AI Agent Definition ---

class PydanticKGAgent:
    def __init__(self, api_key: str):
        self.model = GoogleModel('gemini-2.5-flash')
        
        self.kg_agent = Agent(
            model=self.model,
            output_type=KnowledgeExtraction,
            system_prompt=(
                "You are an expert Knowledge Graph Architect. Analyze the provided text and distill "
                "the essential knowledge.\n\n"
                "1. Identify the primary Hubs, Concepts, and Technologies.\n"
                "2. For each, provide a brief, educational description.\n"
                "3. Extract the most important explanatory excerpts (complete thoughts/code blocks).\n\n"
                "CRITICAL INSTRUCTION: Before creating a new Hub or Concept, ALWAYS use the provided tools "
                "to check what already exists in the vault. Strongly prefer linking to existing Hubs/Concepts "
                "instead of creating near-duplicates. "
            )
        )
        
        @self.kg_agent.tool_plain
        def list_existing_hubs() -> list[str]:
            """Get a list of all existing Hubs in the knowledge graph. Call this before defining a new Concept's parent hub."""
            if not HUBS_DIR.exists(): return []
            return [p.stem.replace('_', ' ') for p in HUBS_DIR.glob("*.md")]

        @self.kg_agent.tool_plain
        def list_existing_concepts() -> list[str]:
            """Get a list of all existing Concepts in the knowledge graph. Call this before defining a new Technology's parent concept."""
            if not CONCEPTS_DIR.exists(): return []
            return [p.stem.replace('_', ' ') for p in CONCEPTS_DIR.glob("*.md")]
        
        # Ensure directories exist
        for d in [HUBS_DIR, CONCEPTS_DIR, TECH_DIR, PROCESSED_TRANSCRIPTS_DIR]:
            d.mkdir(parents=True, exist_ok=True)

    def run_full_pass(self):
        print("\n--- Starting Pydantic KG Agent Pass ---")
        self.process_inbox()
        print("--- Pydantic KG Agent Pass Complete ---")

    def process_inbox(self):
        inbox_files = [p for p in INBOX_DIR.glob('**/*') if p.is_file() and p.suffix.lower() in ['.md', '.txt']]
        
        if not inbox_files:
            print("Inbox is empty.")
            return

        for file_path in inbox_files:
            print(f"  Processing: {file_path.name}")
            try:
                self.process_single_note(file_path)
                new_path = PROCESSED_TRANSCRIPTS_DIR / file_path.name
                file_path.rename(new_path)
                print(f"  Moved to: {new_path}")
            except Exception as e:
                print(f"  ERROR processing {file_path.name}: {e}")

    def process_single_note(self, note_path):
        with open(note_path, "r", encoding='utf-8') as f:
            content = f.read()

        print("    -> Analyzing note and calling tools via Pydantic AI...")
        result = self.kg_agent.run_sync(content)
        extracted_data: KnowledgeExtraction = result.output
        
        print("    -> LLM Analysis complete. Writing nodes to vault...")
        self.create_or_update_nodes(extracted_data, note_path)

    def create_or_update_nodes(self, data: KnowledgeExtraction, source_note_path: Path):
        source_link = f"[[{PROCESSED_TRANSCRIPTS_DIR.name}/{source_note_path.name}]]"

        # Create Hubs
        for hub in data.hubs:
            hub_name = sanitize_filename(hub.name)
            hub_path = HUBS_DIR / f"{hub_name}.md"
            self._create_note_if_not_exists(
                path=hub_path,
                template=HUB_TEMPLATE,
                title=hub.name.replace('_', ' '),
                description=hub.description,
                tag=hub_name.lower(),
                source=source_link,
                excerpts=hub.excerpts
            )

        # Create Concepts
        for concept in data.concepts:
            concept_name = sanitize_filename(concept.name)
            concept_path = CONCEPTS_DIR / f"{concept_name}.md"
            
            hub_name = sanitize_filename(concept.parent_hub)
            hub_path = HUBS_DIR / f"{hub_name}.md"
            hub_link = f"[[{hub_path.parent.name}/{hub_path.stem}]]" if hub_name else ""
            
            self._create_note_if_not_exists(
                path=concept_path,
                template=CONCEPT_TEMPLATE,
                title=concept.name.replace('_', ' '),
                description=concept.description,
                hub=hub_link,
                tag=concept_name.lower(),
                source=source_link,
                excerpts=concept.excerpts
            )
            
            if hub_name and hub_path.exists():
                concept_link = f"- [[{concept_path.parent.name}/{concept_path.stem}]]"
                self._append_link(hub_path, "## Concepts", concept_link)

        # Create Technologies
        for tech in data.technologies:
            tech_name = sanitize_filename(tech.name)
            tech_path = TECH_DIR / f"{tech_name}.md"

            concept_name = sanitize_filename(tech.parent_concept)
            concept_path = CONCEPTS_DIR / f"{concept_name}.md"
            concept_link = f"[[{concept_path.parent.name}/{concept_path.stem}]]" if concept_name else ""

            self._create_note_if_not_exists(
                path=tech_path,
                template=TECHNOLOGY_TEMPLATE,
                title=tech.name.replace('_', ' '),
                description=tech.description,
                concept=concept_link,
                source=source_link,
                tag=tech_name.lower(),
                excerpts=tech.excerpts
            )

            if concept_name and concept_path.exists():
                tech_link = f"- [[{tech_path.parent.name}/{tech_path.stem}]]"
                self._append_link(concept_path, "## Technologies", tech_link)
            
            self._append_link(tech_path, "### Source", f"*   Original reference: {source_link}")

    # --- Reused Vault Utility Functions ---

    def _create_note_if_not_exists(self, path, template, **kwargs):
        if not path.exists():
            print(f"    Creating new note: {path.name}")
            content = template.format(**kwargs)
            with open(path, "w", encoding='utf-8') as f:
                f.write(content)

            self._append_info_block(path, kwargs.get("source", ""), kwargs.get("excerpts", []))
        else:
            print(f"    Note already exists: {path.name}")
            if "source" in kwargs:
                self._append_info_block(path, kwargs["source"], kwargs.get("excerpts", []))

    def _append_info_block(self, file_path, source_link, excerpts):
        if not file_path.exists() or not excerpts:
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        info_block_header = f"> From: {source_link} (Added on {timestamp})"
        
        with open(file_path, "r+", encoding='utf-8') as f:
            content_str = f.read()

            if info_block_header in content_str:
                return

            lines = content_str.splitlines()
            try:
                section_line_index = next(i for i, line in enumerate(lines) if line.strip() == "## Excerpts & Key Information")
                
                insert_index = section_line_index + 1
                while insert_index < len(lines) and (lines[insert_index].strip().startswith('>') or lines[insert_index].strip() == "" or lines[insert_index].strip().startswith('-')):
                    insert_index += 1

                block_to_insert_lines = [f"\n{info_block_header}\n"]
                for excerpt in excerpts:
                    if self._is_code_snippet(excerpt):
                        block_to_insert_lines.append(f"```python\n{excerpt}\n```\n")
                    else:
                        block_to_insert_lines.append(f"*   {excerpt}\n")
                block_to_insert_lines.append("\n")

                lines[insert_index:insert_index] = block_to_insert_lines

                f.seek(0)
                f.write("\n".join(lines))
            except StopIteration:
                f.seek(0, 2)
                f.write(f"\n\n## Excerpts & Key Information\n")
                f.write(f"\n{info_block_header}\n")
                for excerpt in excerpts:
                    if self._is_code_snippet(excerpt):
                        f.write(f"```python\n{excerpt}\n```\n")
                    else:
                        f.write(f"*   {excerpt}\n")
                f.write("\n")

    def _is_code_snippet(self, text):
        python_patterns = [
            r'^\s*def\s+\w+\s*\(', r'^\s*class\s+\w+', r'^\s*import\s+\w+', 
            r'^\s*from\s+\w+\s+import\b', r'^\s*@\w+', r'^\s*if\s+__name__\s*==\s*[\'"]__main__[\'"]\s*:', 
            r'^\s*for\s+\w+\s+in\s+.*:', r'^\s*try:', r'^\s*except\b.*:'
        ]
        bash_patterns = [
            r'^#!\s*(/usr)?/bin/(env\s+)?(bash|sh|zsh)', r'^\s*export\s+\w+=', 
            r'^\s*(sudo\s+|apt(-get)?\s+|pip\s+|npm\s+|docker\s+|kubectl\s+|git\s+)', 
            r'^\s*if\s+\[\s+.*\s+\]\s*;\s*then', r'^\s*for\s+\w+\s+in\s+.*\s*;\s*do', r'^\s*\$\s+'
        ]

        for pattern in python_patterns + bash_patterns:
            if re.search(pattern, text, re.MULTILINE):
                return True

        lines = [line for line in text.splitlines() if line.strip()]
        if len(lines) >= 3:
            indented_lines = sum(1 for line in lines if line.startswith('    ') or line.startswith('\t'))
            if indented_lines / len(lines) > 0.7:
                return True
        return False

    def _append_link(self, file_path, section_heading, link_to_add):
        if not file_path.exists(): return

        with open(file_path, "r+", encoding='utf-8') as f:
            content = f.read()
            if link_to_add in content: return
            
            lines = content.splitlines()
            try:
                section_line_index = next(i for i, line in enumerate(lines) if line.strip() == section_heading)
                insert_index = section_line_index + 1
                while insert_index < len(lines) and (lines[insert_index].strip().startswith('-') or lines[insert_index].strip() == ""):
                    insert_index += 1
                lines.insert(insert_index, link_to_add)
                f.seek(0)
                f.write("\n".join(lines))
            except StopIteration:
                f.seek(0, 2)
                f.write(f"\n\n{section_heading}\n{link_to_add}\n")

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("ERROR: Please set the GEMINI_API_KEY environment variable.")
    else:
        agent = PydanticKGAgent(api_key=api_key)
        agent.run_full_pass()
