import os
import re
import json
from pathlib import Path
from dotenv import load_dotenv
from datetime import datetime

import google.generativeai as genai # Reverted to match installed package

# --- Constants and Configuration ---

VAULT_ROOT = Path("/home/lukasz/Documents/ObsidianVault")
AGENT_DIR = VAULT_ROOT / "Agents"
INBOX_DIR = VAULT_ROOT / "Inbox"
RESOURCES_DIR = VAULT_ROOT / "Resources"
PROJECTS_DIR = VAULT_ROOT / "Projects"
ARCHIVES_DIR = VAULT_ROOT / "Archives" / "Retired_Assets"
PROCESSED_TRANSCRIPTS_DIR = RESOURCES_DIR / "Processed_Transcripts"

# Note templates
HUB_TEMPLATE = """---\ntype: \"Hub\"
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

CONCEPT_TEMPLATE = """---\ntype: \"Concept\"
hub: \"{hub}\"\ntags: [concept, {tag}]
---
# {title}

{description}

## Technologies
- 

## Excerpts & Key Information

## Further Reading

> Core Node: [[Projects/Second_Brain]]
"""

TECHNOLOGY_TEMPLATE = """---\ntype: \"Technology\"
concept: \"{concept}\"\ntags: [technology, {tag}]
---
# {title}

{description}

## Excerpts & Key Information

## Further Reading

### Source
*   Original reference: {source}

> Core Node: [[Projects/Second_Brain]]
"""

# --- Main Agent Class ---

class KnowledgeGraphAgent:
    def _sanitize_filename(self, name):
        """Converts a string to Title_Case_With_Underscores format."""
        # Convert to title case
        name = name.title()
        # Replace spaces and hyphens with underscores
        name = re.sub(r'[ -]', '_', name)
        # Remove any non-alphanumeric characters except underscores
        name = re.sub(r'[^a-zA-Z0-9_]', '', name)
        return name

    def __init__(self, api_key):
        """Initializes the agent, configures the Gemini API."""
        self.vault_root = VAULT_ROOT
        # Reverted to the correct initialization for google.generativeai
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.persona = ""
        self.instructions = ""
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_tokens = 0

    def load_instructions(self):
        """
        Loads the persona and agent instructions from the vault.
        """
        print("Loading agent instructions and persona...")
        with open(AGENT_DIR / "Persona.md", "r") as f:
            self.persona = f.read()
        with open(AGENT_DIR / "Knowledge_Graph_Agent_Instructions.md", "r") as f:
            self.instructions = f.read()
        print("Instructions loaded.")

    def run_full_pass(self):
        """
        Executes a full pass of the agent's workflow as defined in the mandate.
        """
        print("\n--- [DEBUG] Starting New Agent Pass ---")
        self.load_instructions()

        # 1. Process Inbox
        print("\n--- [DEBUG] Starting Inbox Processing ---")
        self.process_inbox()
        print("--- [DEBUG] Finished Inbox Processing ---")

        # 2. Vault-wide Audit
        print("\n--- [DEBUG] Starting Vault Audit ---")
        self.audit_vault_connectivity()
        self.merge_duplicates()
        self.enforce_conventions()
        print("--- [DEBUG] Finished Vault Audit ---")

        print("\n--- Token Usage Report ---")
        print(f"  - Prompt Tokens: {self.total_prompt_tokens}")
        print(f"  - Completion Tokens: {self.total_completion_tokens}")
        print(f"  - Total Tokens for this run: {self.total_tokens}")
        print("--------------------------")

        print("--- Agent Pass Complete ---")

    def process_inbox(self):
        """
        Processes all files in the Inbox directory, now handling spaces in filenames.
        """
        print("--- [DEBUG] Inside process_inbox ---")
        # A more robust way to get all files, including those with spaces
        inbox_files = [p for p in INBOX_DIR.glob('**/*') if p.is_file() and p.suffix.lower() in ['.md', '.txt']]
        print(f"--- [DEBUG] Found {len(inbox_files)} files in Inbox: {[p.name for p in inbox_files]} ---")

        if not inbox_files:
            print("Inbox is empty.")
            return

        for file_path in inbox_files:
            print(f"  Processing: {file_path.name}")
            try:
                self.process_single_note(file_path)
                # Move to processed transcripts after successful processing
                new_path = PROCESSED_TRANSCRIPTS_DIR / file_path.name
                file_path.rename(new_path)
                print(f"  Moved to: {new_path}")
            except Exception as e:
                print(f"  ERROR processing {file_path.name}: {e}")

    def process_single_note(self, note_path):
        """
        Uses the LLM to analyze a single note and create/link knowledge nodes.
        """
        with open(note_path, "r", encoding='utf-8') as f:
            content = f.read()

        prompt = f"""
        {self.persona}

        {self.instructions}

        **Task:**
        Analyze the following text from the note titled '{note_path.stem}'. Your goal is to **distill the essential knowledge** from this text.

        1.  Identify the primary Hubs, Concepts, and Technologies.
        2.  For each, provide a brief, persona-aligned description.
        3.  For each, **extract the most important and explanatory excerpts**. These are the core teachings of the source note.
            *   For **textual explanations** (definitions, principles, arguments), capture the **complete thought or process**, even if it spans multiple sentences.
            *   For **code examples**, extract the **entire relevant code block verbatim**, including any comments.
            *   Do not be limited to 3 excerpts; extract all information that is critical for understanding the topic.

        Return the output ONLY as a valid JSON object.
        The JSON should have three keys: "hubs", "concepts", and "technologies".
        - "hubs" should be a list of objects, each with "name", "description", and an optional list of "excerpts" (strings).
        - "concepts" should be a list of objects, each with "name", "description", a "hub" (the name of its parent hub), and an optional list of "excerpts" (strings).
        - "technologies" should be a list of objects, each with "name", "description", a "concept" (the name of its parent concept), and an optional list of "excerpts" (strings).

        **Example JSON Output:**
        ```json
        {{
          "hubs": [
            {{
              "name": "Cloud_Engineering",
              "description": "The discipline of designing, building, and maintaining cloud-based infrastructure and services, crucial for scalable AI deployment.",
              "excerpts": ["Cloud engineering is essential for scalable AI deployment."]
            }}
          ],
          "concepts": [
            {{
              "name": "Load_Balancing",
              "description": "The process of distributing network traffic across multiple servers to ensure high availability and reliability for production systems.",
              "hub": "Cloud_Engineering",
              "excerpts": ["Load balancing distributes traffic across multiple servers."]
            }}
          ],
          "technologies": [
            {{
              "name": "AWS_ELB",
              "description": "Amazon Web Services' Elastic Load Balancing, a managed service for automatically distributing incoming application traffic.",
              "concept": "Load_Balancing",
              "excerpts": ["AWS ELB distributes incoming application traffic."]
            }}
          ]
        }}
        ```

        **Text to Analyze:**
        ---
        {content}
        ---
        """

        response = self.model.generate_content(prompt)
        
        # Track token usage
        if hasattr(response, 'usage_metadata'):
            usage_metadata = response.usage_metadata
            self.total_prompt_tokens += usage_metadata.prompt_token_count
            self.total_completion_tokens += usage_metadata.candidates_token_count
            self.total_tokens += usage_metadata.total_token_count
            print(f"    Tokens used for this note: {usage_metadata.total_token_count}")

        cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        
        try:
            extracted_data = json.loads(cleaned_response)
            print(f"    LLM Analysis complete.")
            self.create_or_update_nodes(extracted_data, note_path)
        except json.JSONDecodeError as e:
            print(f"    ERROR: Could not decode LLM response: {e}")
            print(f"    Raw Response: {response.text}")

    def create_or_update_nodes(self, data, source_note_path):
        """
        Creates or updates the knowledge graph notes and links them, with validation.
        """
        source_link = f"[[{PROCESSED_TRANSCRIPTS_DIR.name}/{source_note_path.name}]]"

        try:
            # Create Hubs
            for hub_data in data.get("hubs", []):
                if not hub_data.get("name"):
                    print("    Skipping hub with no name.")
                    continue
                hub_name = self._sanitize_filename(hub_data["name"])
                hub_path = RESOURCES_DIR / "Hubs" / f"{hub_name}.md"
                self._create_note_if_not_exists(
                    path=hub_path,
                    template=HUB_TEMPLATE,
                    title=hub_data["name"].replace('_', ' '),
                    description=hub_data.get("description", ""),
                    tag=hub_name.lower(),
                    source=source_link,
                    excerpts=hub_data.get("excerpts", [])
                )

            # Create Concepts and link them to Hubs
            for concept_data in data.get("concepts", []):
                if not concept_data.get("name"):
                    print("    Skipping concept with no name.")
                    continue
                concept_name = self._sanitize_filename(concept_data["name"])
                concept_path = RESOURCES_DIR / "Concepts" / f"{concept_name}.md"
                
                hub_name_str = concept_data.get("hub", "")
                if not hub_name_str:
                    print(f"    Skipping linking for concept '{concept_name}' as it has no parent hub.")
                    hub_link = ""
                    hub_path = None
                else:
                    hub_name = self._sanitize_filename(hub_name_str)
                    hub_path = RESOURCES_DIR / "Hubs" / f"{hub_name}.md"
                    hub_link = f"[[{hub_path.parent.name}/{hub_path.stem}]]"
                
                self._create_note_if_not_exists(
                    path=concept_path,
                    template=CONCEPT_TEMPLATE,
                    title=concept_data["name"].replace('_', ' '),
                    description=concept_data.get("description", ""),
                    hub=hub_link,
                    tag=concept_name.lower(),
                    source=source_link,
                    excerpts=concept_data.get("excerpts", [])
                )
                
                if hub_path and hub_path.exists():
                    concept_link = f"- [[{concept_path.parent.name}/{concept_path.stem}]]"
                    self._append_link(hub_path, "## Concepts", concept_link)

            # Create Technologies and link them to Concepts
            for tech_data in data.get("technologies", []):
                if not tech_data.get("name"):
                    print("    Skipping technology with no name.")
                    continue
                tech_name = self._sanitize_filename(tech_data["name"])
                tech_path = RESOURCES_DIR / "Technologies" / f"{tech_name}.md"

                concept_name_str = tech_data.get("concept", "")
                if not concept_name_str:
                    print(f"    Skipping linking for technology '{tech_name}' as it has no parent concept.")
                    concept_link = ""
                    concept_path = None
                else:
                    concept_name = self._sanitize_filename(concept_name_str)
                    concept_path = RESOURCES_DIR / "Concepts" / f"{concept_name}.md"
                    concept_link = f"[[{concept_path.parent.name}/{concept_path.stem}]]"

                self._create_note_if_not_exists(
                    path=tech_path,
                    template=TECHNOLOGY_TEMPLATE,
                    title=tech_data["name"].replace('_', ' '),
                    description=tech_data.get("description", ""),
                    concept=concept_link,
                    source=source_link,
                    tag=tech_name.lower(),
                    excerpts=tech_data.get("excerpts", [])
                )

                if concept_path and concept_path.exists():
                    tech_link = f"- [[{tech_path.parent.name}/{tech_path.stem}]]"
                    self._append_link(concept_path, "## Technologies", tech_link)
                
                self._append_link(tech_path, "### Source", f"*   Original reference: {source_link}")
        except Exception as e:
            print(f"    ERROR during node creation/linking: {e}")

    def _create_note_if_not_exists(self, path, template, **kwargs):
        """
        Creates a note from a template if it doesn't already exist, and enriches it.
        """
        if not path.exists():
            print(f"    Creating new note: {path.name}")
            content = template.format(**kwargs)
            with open(path, "w", encoding='utf-8') as f:
                f.write(content)

            self._append_info_block(path, kwargs.get("source", ""), kwargs.get("excerpts", []))

            try:
                print(f"      -> Searching for further reading on '{kwargs['title']}'...")
                search_results = [
                    {"url": f"https://www.google.com/search?q={kwargs['title'].replace(' ', '+')}", "title": f"Google Search: {kwargs['title']}"}
                ]
                
                if search_results:
                    for result in search_results[:2]:
                        link = f"-[{result['title']}]({result['url']})"
                        self._append_link(path, "## Further Reading", link)
            except Exception as e:
                print(f"      -> Web search failed: {e}")
        else:
            print(f"    Note already exists: {path.name}")
            if "source" in kwargs:
                self._append_info_block(path, kwargs["source"], kwargs.get("excerpts", []))

    def _append_info_block(self, file_path, source_link, excerpts):
        """
        Appends a timestamped info block (source and excerpts) to a note's 'Excerpts & Key Information' section.
        Formats excerpts as code blocks or list items, preventing duplicate entries.
        """
        if not file_path.exists() or not excerpts:
            return

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        info_block_header = f"> From: {source_link} (Added on {timestamp})"
        
        with open(file_path, "r+", encoding='utf-8') as f:
            content_str = f.read()

            # Check for header to prevent duplicates
            if info_block_header in content_str:
                return

            lines = content_str.splitlines()
            try:
                section_line_index = next(i for i, line in enumerate(lines) if line.strip() == "## Excerpts & Key Information")
                
                insert_index = section_line_index + 1
                # Skip any existing lines in this section to append new info at the end of it
                while insert_index < len(lines) and (lines[insert_index].strip().startswith('>') or lines[insert_index].strip() == "" or lines[insert_index].strip().startswith('-')):
                    insert_index += 1

                # Prepare the full block to insert
                block_to_insert_lines = [f"\n{info_block_header}\n"] # Header with blank lines around it
                for excerpt in excerpts:
                    if self._is_code_snippet(excerpt):
                        block_to_insert_lines.append(f"```python\n{excerpt}\n```\n")
                    else:
                        block_to_insert_lines.append(f"*   {excerpt}\n")
                block_to_insert_lines.append("\n") # Final blank line after the block

                lines[insert_index:insert_index] = block_to_insert_lines # Insert the list of lines

                f.seek(0)
                f.write("\n".join(lines))
                print(f"      -> Added excerpts from {source_link.split('/')[-1][:-2]} to {file_path.name}")

            except StopIteration:
                # Fallback if section not found
                f.seek(0, 2)
                f.write(f"\n\n## Excerpts & Key Information\n")
                f.write(f"\n{info_block_header}\n")
                for excerpt in excerpts:
                    if self._is_code_snippet(excerpt):
                        f.write(f"```python\n{excerpt}\n```\n")
                    else:
                        f.write(f"*   {excerpt}\n")
                f.write("\n")
                print(f"      -> Added excerpts from {source_link.split('/')[-1][:-2]} to {file_path.name}")

    def _is_code_snippet(self, text):
        """
        A heuristic to guess if a string is a Python or Bash code snippet,
        minimizing false positives from regular text.
        """
        # Strong Python markers
        python_patterns = [
            r'^\s*def\s+\w+\s*\(',              # Function definition
            r'^\s*class\s+\w+',                 # Class definition
            r'^\s*import\s+\w+',                # Import statement
            r'^\s*from\s+\w+\s+import\b',       # From-import statement
            r'^\s*@\w+',                        # Decorator
            r'^\s*if\s+__name__\s*==\s*[\'"]__main__[\'"]\s*:', # Main block
            r'^\s*for\s+\w+\s+in\s+.*:',        # For loop
            r'^\s*try:',                        # Try block
            r'^\s*except\b.*:',                 # Except block
        ]

        # Strong Bash markers
        bash_patterns = [
            r'^#!\s*(/usr)?/bin/(env\s+)?(bash|sh|zsh)', # Shebang
            r'^\s*export\s+\w+=',               # Export variable
            r'^\s*(sudo\s+|apt(-get)?\s+|pip\s+|npm\s+|docker\s+|kubectl\s+|git\s+)', # Common CLI commands
            r'^\s*if\s+\[\s+.*\s+\]\s*;\s*then', # Bash if
            r'^\s*for\s+\w+\s+in\s+.*\s*;\s*do', # Bash for
            r'^\s*\$\s+',                       # Terminal prompt start
        ]

        for pattern in python_patterns + bash_patterns:
            if re.search(pattern, text, re.MULTILINE):
                return True

        # Indentation check for multi-line snippets
        lines = [line for line in text.splitlines() if line.strip()]
        if len(lines) >= 3:
            indented_lines = sum(1 for line in lines if line.startswith('    ') or line.startswith('\t'))
            if indented_lines / len(lines) > 0.7:
                return True

        return False

    def _append_link(self, file_path, section_heading, link_to_add):
        """Appends a markdown link to a specific section of a file if it's not already there."""
        if not file_path.exists():
            return

        with open(file_path, "r+", encoding='utf-8') as f:
            content = f.read()
            if link_to_add in content:
                return
            
            lines = content.splitlines()
            try:
                section_line_index = next(i for i, line in enumerate(lines) if line.strip() == section_heading)
                
                insert_index = section_line_index + 1
                while insert_index < len(lines) and (lines[insert_index].strip().startswith('-') or lines[insert_index].strip() == ""):
                    insert_index += 1
                
                lines.insert(insert_index, link_to_add)
                f.seek(0)
                f.write("\n".join(lines))
                link_name_for_print = link_to_add.split('/')[-1].replace(']]', '').replace(')', '').strip()
                print(f"      -> Linked {link_name_for_print} to {file_path.name}")

            except StopIteration:
                f.seek(0, 2)
                f.write(f"\n\n{section_heading}\n{link_to_add}\n")
                link_name_for_print = link_to_add.split('/')[-1].replace(']]', '').replace(')', '').strip()
                print(f"      -> Linked {link_name_for_print} to {file_path.name}")

    def audit_vault_connectivity(self):
        """
        Finds notes with few outgoing links.
        """
        print("\nAuditing vault connectivity...")
        scan_dirs = [
            RESOURCES_DIR / "Hubs", 
            RESOURCES_DIR / "Concepts", 
            RESOURCES_DIR / "Technologies"
        ]
        
        for directory in scan_dirs:
            for note_path in directory.glob("*.md"):
                with open(note_path, "r", encoding='utf-8') as f:
                    content = f.read()
                
                links = re.findall(r'\[\[(.*?)\]\]', content)
                if "Projects/Second_Brain" in links:
                    links.remove("Projects/Second_Brain")

                if len(links) < 2:
                    print(f"  - Weakly linked note found: {note_path.name} (Links: {len(links)})")

    def merge_duplicates(self):
        """
        Finds and reports potential duplicate notes based on substring matching of normalized names.
        """
        print("\nChecking for potential duplicates...")
        
        notes_with_normalized_names = {}
        scan_dirs = [
            RESOURCES_DIR / "Hubs", 
            RESOURCES_DIR / "Concepts", 
            RESOURCES_DIR / "Technologies"
        ]

        for directory in scan_dirs:
            for note_path in directory.glob("*.md"):
                normalized = note_path.stem.replace('_', '').lower()
                notes_with_normalized_names[note_path.name] = normalized

        potential_duplicates = {}
        note_names = list(notes_with_normalized_names.keys())

        for i in range(len(note_names)):
            for j in range(i + 1, len(note_names)):
                name1 = note_names[i]
                norm1 = notes_with_normalized_names[name1]
                
                name2 = note_names[j]
                norm2 = notes_with_normalized_names[name2]

                if norm1 in norm2 or norm2 in norm1:
                    key = tuple(sorted((name1, name2)))
                    if key not in potential_duplicates:
                        potential_duplicates[key] = {name1, name2}

        if not potential_duplicates:
            print("  - No potential duplicates found.")
        else:
            for key, files in potential_duplicates.items():
                 print(f"  - Potential duplicate set found: {list(files)}")

    def enforce_conventions(self):
        """
        Enforces vault conventions, such as adding the Core Node footer.
        """
        print("\nEnforcing vault conventions...")
        all_notes = list(VAULT_ROOT.glob("**/*.md"))
        core_node_text = "> Core Node: [[Projects/Second_Brain]]"

        for note_path in all_notes:
            if ".venv" in str(note_path):
                continue

            with open(note_path, "r+", encoding='utf-8') as f:
                content = f.read()
                if core_node_text not in content:
                    f.seek(0, 2)
                    f.write(f"\n\n{core_node_text}\n")
                    print(f"  - Added Core Node footer to: {note_path.name}")

# --- Main Execution ---

if __name__ == "__main__":
    print("--- [DEBUG] Script execution started ---")
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: Please set the GEMINI_API_KEY environment variable.")
    else:
        agent = KnowledgeGraphAgent(api_key=api_key)
        agent.run_full_pass()
