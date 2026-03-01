
import os
import re
import json
from pathlib import Path
from dotenv import load_dotenv
import subprocess
import shutil

import google.generativeai as genai

# --- Constants and Configuration ---

VAULT_ROOT = Path("/home/lukasz/Documents/ObsidianVault")
AGENT_DIR = VAULT_ROOT / "Agents"
BOOKS_INBOX_DIR = VAULT_ROOT / "Books" / "Inbox"
BOOKS_SUMMARIES_DIR = VAULT_ROOT / "Books" / "Summaries"
MAIN_INBOX_DIR = VAULT_ROOT / "Inbox"
PROCESSED_BOOKS_DIR = VAULT_ROOT / "Archives" / "Processed_Books"

SUMMARY_TEMPLATE = """---
type: "book-summary"
author: "{author}"
source_file: "{source_file}"
tags: [book-summary, {tags}]
---

# Summary: {title}

## High-Level Summary

{high_level_summary}

## Core Themes

{core_themes}

## Key Learnings & Concepts

{key_learnings}
"""

# --- Main Agent Class ---

class BookAgent:
    def __init__(self, api_key):
        """Initializes the agent and configures the Gemini API."""
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        self.total_tokens = 0

    def run(self):
        """Runs the full book processing workflow."""
        print("\n--- Starting Book Agent Pass ---")
        self.process_book_inbox()
        print("\n--- Token Usage Report ---")
        print(f"  - Total Tokens for this run: {self.total_tokens}")
        print("--------------------------")
        print("--- Book Agent Pass Complete ---")

    def process_book_inbox(self):
        """Processes all PDF files in the Books/Inbox directory."""
        print("Scanning for new books...")
        book_files = list(BOOKS_INBOX_DIR.glob("*.pdf"))
        
        if not book_files:
            print("No new books to process.")
            return

        for book_path in book_files:
            print(f"  Processing book: {book_path.name}")
            try:
                # 1. Extract text with pdftotext
                print("    -> Extracting text with pdftotext...")
                text_content = self.extract_text_from_pdf(book_path)
                
                # Truncate for safety and cost control (adjust as needed)
                if len(text_content) > 500000:
                    print(f"    -> Warning: Text is very long ({len(text_content)} chars). Truncating to 500k chars.")
                    text_content = text_content[:500000]

                # 2. Generate summary with AI
                print("    -> Generating summary with Gemini API...")
                summary_data = self.generate_summary(text_content)

                # 3. Create and save the Markdown note
                print("    -> Creating Markdown summary note...")
                self.create_summary_note(summary_data, book_path)

                # 4. Move the summary to the main Inbox
                summary_filename = f"{book_path.stem}_Summary.md"
                shutil.copy(
                    BOOKS_SUMMARIES_DIR / summary_filename,
                    MAIN_INBOX_DIR / summary_filename
                )
                print(f"    -> Copied summary to main Inbox for Knowledge Graph Agent.")

                # 5. Archive the processed PDF
                book_path.rename(PROCESSED_BOOKS_DIR / book_path.name)
                print(f"    -> Archived processed book to {PROCESSED_BOOKS_DIR.name}")

            except Exception as e:
                print(f"  ERROR processing {book_path.name}: {e}")

    def extract_text_from_pdf(self, pdf_path):
        """Uses the pdftotext shell command to extract text from a PDF."""
        result = subprocess.run(['pdftotext', str(pdf_path), '-'], capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"pdftotext failed: {result.stderr}")
        return result.stdout

    def generate_summary(self, text_content):
        """Sends text to Gemini API for multi-stage summarization."""
        prompt = f"""
        You are an expert analyst. Based on the following text from a book, please perform these tasks:
        1.  Determine the book's title and author.
        2.  Provide a concise, high-level summary of the book's main thesis and arguments.
        3.  Identify the 3-5 most important core themes of the entire book (do not provide chapter-by-chapter summaries). Provide a brief, paragraph-length description for each theme, formatted with markdown headings (e.g., "### Theme Name").
        4.  Extract an exhaustive and highly detailed list of the "Key Learnings & Concepts". This is the most critical part of the summary. Provide deep, actionable insights, complex ideas, and specific takeaways, formatted with markdown bullets (e.g., "*   **Concept:** Detailed, multi-sentence explanation."). Aim for at least 10-15 extensive bullet points.
        5.  Suggest 3-5 relevant tags (as a comma-separated string, e.g., "statistics, forecasting, data-science").

        Return the output ONLY as a valid JSON object with the following keys. All values MUST be strings formatted as Markdown (do NOT return arrays or objects for these fields):
        - "title"
        - "author"
        - "high_level_summary"
        - "core_themes"
        - "key_learnings"
        - "tags"

        **Book Text:**
        ---
        {text_content}
        ---
        """
        response = self.model.generate_content(prompt)
        
        if hasattr(response, 'usage_metadata'):
            self.total_tokens += response.usage_metadata.total_token_count
            print(f"    -> Tokens used for this book: {response.usage_metadata.total_token_count}")

        cleaned_response = response.text.strip().replace("```json", "").replace("```", "").strip()
        return json.loads(cleaned_response)

    def create_summary_note(self, summary_data, source_pdf_path):
        """Formats and saves the summary data into a Markdown file."""
        filename = f"{source_pdf_path.stem}_Summary.md"
        output_path = BOOKS_SUMMARIES_DIR / filename

        def format_field(data):
            if isinstance(data, list):
                formatted = []
                for item in data:
                    if isinstance(item, dict):
                        if 'title' in item and 'summary' in item:
                            formatted.append(f"{item['title']}\n\n{item['summary']}")
                        elif 'concept' in item and 'explanation' in item:
                            formatted.append(f"* **{item['concept']}:** {item['explanation']}")
                        else:
                            formatted.append(str(item))
                    else:
                        formatted.append(str(item))
                return "\n\n".join(formatted)
            return str(data)

        tags_data = summary_data.get("tags", "")
        tags_str = ", ".join(tags_data) if isinstance(tags_data, list) else str(tags_data)

        content = SUMMARY_TEMPLATE.format(
            title=summary_data.get("title", "Unknown Title"),
            author=summary_data.get("author", "Unknown Author"),
            source_file=source_pdf_path.name,
            tags=tags_str,
            high_level_summary=format_field(summary_data.get("high_level_summary", "")),
            core_themes=format_field(summary_data.get("core_themes", "")),
            key_learnings=format_field(summary_data.get("key_learnings", ""))
        )

        with open(output_path, "w", encoding='utf-8') as f:
            f.write(content)
        print(f"    -> Summary saved to: {output_path.name}")

# --- Main Execution ---

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("ERROR: Please set the GEMINI_API_KEY environment variable.")
    else:
        agent = BookAgent(api_key=api_key)
        agent.run()
