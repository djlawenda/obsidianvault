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
    Rewrites relative internal Markdown links to be root-relative.
    Specifically targets patterns observed in warnings.
    """
    with open(file_path, "r", encoding='utf-8') as f:
        content = f.read()

    original_content = content # Keep original to check for changes

    # Regex to find Markdown links and image links: [text](link) or ![text](link)
    # This pattern captures the link path within the parentheses
    link_pattern = re.compile(r'(\]\(|!\[.*?\]\()(.+?)(\))')

    def replace_link(match):
        prefix = match.group(1) # e.g., "](", "![]("
        link_path = match.group(2) # The actual link content
        suffix = match.group(3) # ")"

        # Only process internal links that look like relative paths
        if not link_path.startswith(('http://', 'https://', '#', '/')):
            # Normalize to use / as path separator for consistency
            normalized_link_path = Path(link_path).as_posix()
            
            # Resolve to be relative to VAULT_ROOT first, then to DOCS_DIR
            # This handles cases like '../../Processed_Transcripts/File.md'
            # and converts them to '/Resources/Processed_Transcripts/File.md'
            
            # Construct absolute path based on original file's assumed location relative to VAULT_ROOT
            # and then get the path relative to VAULT_ROOT, then prepend '/'
            
            # Example: For a file in docs/Resources/Concepts/A.md linking to ../../Projects/B.md
            # 1. Original source was VAULT_ROOT/Resources/Concepts/A.md
            # 2. Link target relative to original source: ../../Projects/B.md
            # 3. Absolute path of target in vault: VAULT_ROOT/Projects/B.md
            # 4. Path relative to VAULT_ROOT: Projects/B.md
            # 5. Desired link in MkDocs: /Projects/B.md (root-relative to docs)

            # Determine the original source directory for the current Markdown file
            # This is key to correctly resolving relative links in the source
            doc_relative_to_vault = file_path.relative_to(DOCS_DIR)
            original_source_file_path = VAULT_ROOT / doc_relative_to_vault
            original_source_dir = original_source_file_path.parent

            try:
                # Resolve the target path relative to the original source directory
                resolved_abs_path_in_vault = (original_source_dir / normalized_link_path).resolve()
                
                # Get the path relative to VAULT_ROOT
                resolved_relative_to_vault_root = resolved_abs_path_in_vault.relative_to(VAULT_ROOT)
                
                # Construct the new root-relative path for MkDocs
                new_link_path = "/" + resolved_relative_to_vault_root.as_posix()
                
                # Ensure it points to an .md file, removing extension if roamlinks handles it
                if new_link_path.endswith('.md'):
                    new_link_path = new_link_path[:-3] + '/' # Convert .md to / for clean URLs
                                                              # with index.md or auto-generated index
                # Special handling for "Second_Brain.md" which should be '/Projects/Second_Brain/'
                # And Processed_Transcripts which should be '/Resources/Processed_Transcripts/.../'
                if 'second_brain' in new_link_path.lower():
                     new_link_path = "/Projects/Second_Brain/"
                elif '/processed_transcripts/' in new_link_path.lower():
                    # Ensure correct path if it was e.g. /Resources/Processed_Transcripts/File
                    parts = new_link_path.split('/Processed_Transcripts/')
                    if len(parts) > 1:
                        file_name = parts[1].strip('/')
                        if file_name:
                            new_link_path = f"/Resources/Processed_Transcripts/{file_name}/"
                    
                # The roamlinks plugin will convert [[Note Name]]
                # For regular Markdown links, we need to ensure the path is correct
                
                print(f"      Rewriting link in {file_path.name}: '{link_path}' -> '{new_link_path}'")
                return f"{prefix}{new_link_path}{suffix}"
            except ValueError as e:
                print(f"      Warning: Could not rewrite link '{link_path}' in {file_path.name}: {e}")
                # If resolution fails, return original link path to avoid breaking
                return f"{prefix}{link_path}{suffix}"
        
        return f"{prefix}{link_path}{suffix}" # Return original if not an internal relative link

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
        # Determine the section (e.g., Resources, Books, Projects)
        try:
            # Look for the first directory part that matches a SOURCE_DIR prefix
            for source_root_path in SOURCE_DIRS:
                if path.is_relative_to(DOCS_DIR / source_root_path.name):
                    section_name = source_root_path.name
                    break
            else: # If no specific source_root_path matches, put it at the root of nav
                section_name = "" 
            
            if section_name:
                relative_to_section = path.relative_to(DOCS_DIR / section_name)
                parts = (section_name,) + relative_to_section.parts
            else:
                parts = path.relative_to(DOCS_DIR).parts
        except ValueError: # path is not relative to DOCS_DIR / source_root_path.name
            parts = path.relative_to(DOCS_DIR).parts
        
        current_level = nav_entries
        for part in parts[:-1]: # Iterate through directories
            if part not in current_level:
                current_level[part] = {}
            current_level = current_level[part]
        
        # Add file, using stem for title and root-relative path for MkDocs
        file_title = path.stem.replace('_', ' ').replace('-', ' ').title()
        
        # Ensure path is always root-relative to docs and ends with / for directory-style links
        mkdocs_path = "/" + str(path.relative_to(DOCS_DIR).as_posix())
        if mkdocs_path.endswith('.md'):
            mkdocs_path = mkdocs_path[:-3] + '/' # Convert .md to / for clean URLs

        current_level[file_title] = mkdocs_path

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

    with open(MKDOCS_YML, "w", encoding='utf-8') as f:
        yaml.dump(config, f, sort_keys=False)

if __name__ == "__main__":
    clean_docs_dir()
    copy_notes_to_docs()
    generate_mkdocs_yml()
    print("Documentation build preparation complete. Now run 'mkdocs gh-deploy' to publish.")
