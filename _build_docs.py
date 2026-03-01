import os
import shutil
from pathlib import Path
import yaml
import re # Import re for regular expressions

VAULT_ROOT = Path(__file__).resolve().parent
DOCS_DIR = VAULT_ROOT / "docs"
MKDOCS_YML = VAULT_ROOT / "mkdocs.yml"

# Source directories for notes
SOURCE_DIRS = [
    VAULT_ROOT / "Resources",
    VAULT_ROOT / "Resources" / "Processed_Transcripts", # Explicitly include for clarity
    VAULT_ROOT / "Books" / "Summaries",
    VAULT_ROOT / "Projects", # Include projects folder
]

def clean_docs_dir():
    if DOCS_DIR.exists():
        print(f"Cleaning existing {DOCS_DIR}...\n")
        shutil.rmtree(DOCS_DIR)
    DOCS_DIR.mkdir()

def rewrite_internal_links(file_path: Path):
    """
    Rewrites relative internal Markdown links to be relative to the current file's location
    within the docs/ structure.
    """
    with open(file_path, "r", encoding='utf-8') as f:
        content = f.read()

    original_content = content

    link_pattern = re.compile(r'(\]\(|!\[.*?\]\()(.+?)(\))')

    def replace_link(match):
        prefix = match.group(1)
        link_path = match.group(2)
        suffix = match.group(3)

        # Only process internal links that are not absolute URLs, anchors, or already root-relative
        if not link_path.startswith(('http://', 'https://', '#', '/')):
            normalized_link_path = Path(link_path).as_posix()
            
            try:
                # 1. Determine the original absolute path of the current file in the vault
                doc_relative_to_docs_root = file_path.relative_to(DOCS_DIR)
                original_source_file_in_vault = VAULT_ROOT / doc_relative_to_docs_root
                original_source_dir_in_vault = original_source_file_in_vault.parent

                # 2. Resolve the target link's absolute path within the original vault structure
                resolved_abs_path_in_vault = (original_source_dir_in_vault / normalized_link_path).resolve()

                # 3. Get the target path relative to the current file's directory within DOCS_DIR
                target_path_in_docs = DOCS_DIR / resolved_abs_path_in_vault.relative_to(VAULT_ROOT)
                new_link_path = target_path_in_docs.relative_to(file_path.parent).as_posix()

                # Convert .md extension to / for clean URLs if it's a Markdown file
                if new_link_path.endswith('.md'):
                    new_link_path = new_link_path[:-3] + '/'
                
                print(f"      Rewriting link in {file_path.name}: '{link_path}' -> '{new_link_path}'")
                return f"{prefix}{new_link_path}{suffix}"
            except ValueError as e:
                print(f"      Warning: Could not rewrite link '{link_path}' in {file_path.name}: {e}")
                return f"{prefix}{link_path}{suffix}"
        
        return f"{prefix}{link_path}{suffix}"

    content = link_pattern.sub(replace_link, content)

    if content != original_content:
        with open(file_path, "w", encoding='utf-8') as f:
            f.write(content)
        print(f"  Rewrote internal links in: {file_path.relative_to(DOCS_DIR)}")

def copy_notes_to_docs():
    print("Copying notes to docs/ directory...\n")
    for source_dir in SOURCE_DIRS:
        if not source_dir.exists():
            print(f"  Warning: Source directory not found: {source_dir}")
            continue

        for md_file in source_dir.glob("**/*.md"):
            relative_path = md_file.relative_to(VAULT_ROOT)
            destination_path = DOCS_DIR / relative_path
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(md_file, destination_path)
            print(f"  Copied: {relative_path}")
            
            # After copying, rewrite internal links in the destination file
            rewrite_internal_links(destination_path)
            
    print("\nFinished copying and rewriting links.\n")


def generate_mkdocs_yml():
    print(f"Generating {MKDOCS_YML}...\n")
    config = {
        'site_name': "Obsidian Vault",
        'site_url': "https://djlawenda.github.io/obsidianvault/", # Crucial for GitHub Pages project sites
        'theme': {
            'name': 'material',
            'features': [
                'navigation.tabs',
                'navigation.indexes',
                'toc.integrate',
                'search.suggest',
                'search.highlight',
                'content.tabs.link',
                'content.code.annotate',
                'content.code.copy',
            ],
            'palette': [
                {
                    'scheme': 'default',
                    'primary': 'indigo',
                    'accent': 'indigo',
                    'toggle': {
                        'icon': 'material/brightness-7',
                        'name': 'Switch to dark mode'
                    }
                },
                {
                    'scheme': 'slate',
                    'primary': 'indigo',
                    'accent': 'indigo',
                    'toggle': {
                        'icon': 'material/brightness-4',
                        'name': 'Switch to light mode'
                    }
                }
            ]
        },
        'plugins': [
            'search',
            'roamlinks',
        ],
        'extra': {
            'roamlinks': {
                'strip_brackets': True
            }
        },
        'nav': []
    }

    # Dynamically build navigation from copied files
    nav_entries = {}

    def add_to_nav(path: Path):
        # Get path relative to DOCS_DIR
        relative_doc_path = path.relative_to(DOCS_DIR)
        parts = relative_doc_path.parts # e.g., ('Resources', 'Concepts', 'My_Concept.md')

        current_level = nav_entries
        for part in parts[:-1]: # Iterate through directories
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
        
        # Add file, using stem for title and root-relative path for MkDocs
        file_title = path.stem.replace('_', ' ').replace('-', ' ').title()
        
        # Ensure path is always root-relative to docs and ends with / for directory-style links
        mkdocs_path = "/" + relative_doc_path.as_posix()
        if mkdocs_path.endswith('.md'):
            mkdocs_path = mkdocs_path[:-3] + '/' # Convert .md to / for clean URLs

        print(f"        Adding to nav: Title='{file_title}', Path='{mkdocs_path}'") # ADDED DEBUG PRINT
        current_level[file_title] = mkdocs_path

    for md_file in DOCS_DIR.glob("**/*.md"):
        add_to_nav(md_file)

    def build_mkdocs_nav(data):
        nav = []
        # Sort items: directories first, then files, alphabetically
        sorted_keys = sorted(data.keys(), key=lambda k: (isinstance(data[k], str), k))
        for key in sorted_keys:
            value = data[key]
            if isinstance(value, dict):
                nav.append({key: build_mkdocs_nav(value)})
            else:
                nav.append({key: value})
        return nav
    
    config['nav'] = build_mkdocs_nav(nav_entries)

    with open(MKDOCS_YML, "w", encoding='utf-8') as f:
        yaml.dump(config, f, sort_keys=False)

if __name__ == "__main__":
    clean_docs_dir()
    copy_notes_to_docs()
    generate_mkdocs_yml()
    print("Documentation build preparation complete. Now run 'mkdocs gh-deploy' to publish.")
