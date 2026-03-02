#!/bin/bash
cat << 'EOF_BUILD_DOCS' > /home/lukasz/Documents/ObsidianVault/_build_docs.py
import os
import shutil
from pathlib import Path
import yaml
import re

VAULT_ROOT = Path(__file__).resolve().parent
DOCS_DIR = VAULT_ROOT / "docs"
MKDOCS_YML = VAULT_ROOT / "mkdocs.yml"

SOURCE_DIRS = [
    VAULT_ROOT / "Resources",
    VAULT_ROOT / "Resources" / "Processed_Transcripts",
    VAULT_ROOT / "Books" / "Summaries",
    VAULT_ROOT / "Projects",
]

def clean_docs_dir():
    if DOCS_DIR.exists():
        print(f"Cleaning existing {DOCS_DIR}...
")
        shutil.rmtree(DOCS_DIR)
    DOCS_DIR.mkdir()

def rewrite_internal_links(file_path: Path):
    with open(file_path, "r", encoding='utf-8') as f:
        content = f.read()

    original_content = content
    link_pattern = re.compile(r'(\]\(|!\[.*?\]\()(.+?)(\))')

    def replace_link(match):
        prefix = match.group(1)
        link_path = match.group(2)
        suffix = match.group(3)

        if not link_path.startswith(('http://', 'https://', '#', '/')):
            normalized_link_path = Path(link_path).as_posix()
            
            try:
                doc_relative_to_docs_root = file_path.relative_to(DOCS_DIR)
                original_source_file_in_vault = VAULT_ROOT / doc_relative_to_docs_root
                original_source_dir_in_vault = original_source_file_in_vault.parent

                resolved_abs_path_in_vault = (original_source_dir_in_vault / normalized_link_path).resolve()

                target_path_in_docs = DOCS_DIR / resolved_abs_path_in_vault.relative_to(VAULT_ROOT)
                new_link_path = target_path_in_docs.relative_to(file_path.parent).as_posix()

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
    print("Copying notes to docs/ directory...
")
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
            
            rewrite_internal_links(destination_path)
            
    print("
Finished copying and rewriting links.
")


def generate_mkdocs_yml():
    print(f"Generating {MKDOCS_YML}...
")
    config = {
        'site_name': "Obsidian Vault",
        'site_url': "https://djlawenda.github.io/obsidianvault/",
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
        'nav': [
            { 'Resources': 'Resources/' },
            { 'Books': 'Books/Summaries/' },
            { 'Projects': 'Projects/' },
        ]
    }

    with open(MKDOCS_YML, "w", encoding='utf-8') as f:
        yaml.dump(config, f, sort_keys=False)

if __name__ == "__main__":
    clean_docs_dir()
    copy_notes_to_docs()
    generate_mkdocs_yml()
    print("Documentation build preparation complete. Now run 'mkdocs gh-deploy' to publish.")
EOF_BUILD_DOCS
