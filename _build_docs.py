import os
import shutil
from pathlib import Path
import yaml

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
        print(f"Cleaning existing {DOCS_DIR}...")
        shutil.rmtree(DOCS_DIR)
    DOCS_DIR.mkdir()

def copy_notes_to_docs():
    print("Copying notes to docs/ directory...")
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

def generate_mkdocs_yml():
    print(f"Generating {MKDOCS_YML}...")
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
        parts = path.relative_to(DOCS_DIR).parts
        current_level = nav_entries
        for part in parts[:-1]: # Iterate through directories
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
        
        # Add file, using stem for title and relative_to(DOCS_DIR) for path
        file_title = path.stem.replace('_', ' ').replace('-', ' ').title()
        current_level[file_title] = str(path.relative_to(DOCS_DIR))

    for md_file in DOCS_DIR.glob("**/*.md"):
        add_to_nav(md_file)

    def build_mkdocs_nav(data):
        nav = []
        for key, value in data.items():
            if isinstance(value, dict):
                nav.append({key: build_mkdocs_nav(value)})
            else:
                nav.append({key: value})
        return nav
    
    config['nav'] = build_mkdocs_nav(nav_entries)

    with open(MKDOCS_YML, "w") as f:
        yaml.dump(config, f, sort_keys=False)

if __name__ == "__main__":
    clean_docs_dir()
    copy_notes_to_docs()
    generate_mkdocs_yml()
    print("Documentation build preparation complete. Now run 'mkdocs gh-deploy' to publish.")
