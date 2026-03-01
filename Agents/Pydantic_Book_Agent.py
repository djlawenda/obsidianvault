import os
import shutil
import subprocess
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, Tuple # Import Optional and Tuple

from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel

from Models import BookSummary

# --- Constants and Configuration ---

VAULT_ROOT = Path("/home/lukasz/Documents/ObsidianVault")
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

CHUNK_SIZE = 150000 # Define chunk size here

class PydanticBookAgent:
    def __init__(self, api_key: str):
        # Initialize Google Model via Pydantic AI
        model = GoogleModel('gemini-2.5-flash')
        
        self.agent = Agent(
            model=model,
            output_type=BookSummary,
            system_prompt=(
                "You are an expert analyst. Your task is to extract highly structured "
                "knowledge from book text.\n"
                "1. Identify the book's title and author.\n"
                "2. Provide a concise, high-level summary of the book's main thesis.\n"
                "3. Identify 3-5 core themes of the entire book, providing a brief paragraph for each.\n"
                "4. Extract an exhaustive list (10-15 points) of deep, actionable Key Learnings & Concepts.\n"
                "5. Suggest 3-5 relevant tags."
            )
        )

    def run(self):
        """Runs the full book processing workflow."""
        print("\n--- Starting Pydantic Book Agent Pass ---")
        self.process_book_inbox()
        print("--- Pydantic Book Agent Pass Complete ---")

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
                full_text_length = len(text_content)
                
                if full_text_length > CHUNK_SIZE:
                    print(f"    -> Book is very long ({full_text_length} chars). Chunking into {CHUNK_SIZE} char segments.")
                    
                    chunks = []
                    for i in range(0, full_text_length, CHUNK_SIZE):
                        chunks.append(text_content[i : i + CHUNK_SIZE])
                    
                    total_chunks = len(chunks)
                    for i, chunk in enumerate(chunks):
                        print(f"    -> Generating summary for chunk {i+1} of {total_chunks} with Pydantic AI...")
                        result = self.agent.run_sync(chunk)
                        summary_data: BookSummary = result.output
                        self.create_summary_note(summary_data, book_path, chunk_info=(i + 1, total_chunks))
                else:
                    # Original logic for smaller books
                    print("    -> Generating structured summary with Pydantic AI...")
                    result = self.agent.run_sync(text_content)
                    summary_data: BookSummary = result.output
                    self.create_summary_note(summary_data, book_path)
                
                # 5. Archive the processed PDF (after all chunks are processed, or if it was a single chunk)
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

    def create_summary_note(self, summary: BookSummary, source_pdf_path: Path, chunk_info: Optional[Tuple[int, int]] = None):
        """Formats and saves the BookSummary object into a Markdown file, including chunk info if provided."""
        if chunk_info:
            chunk_num, total_chunks = chunk_info
            filename = f"{source_pdf_path.stem}_part_{chunk_num}_of_{total_chunks}_Summary.md"
        else:
            filename = f"{source_pdf_path.stem}_Summary.md"
        
        output_path = BOOKS_SUMMARIES_DIR / filename

        core_themes_md = "\n\n".join(
            [f"### {theme.name}\n\n{theme.description}" for theme in summary.core_themes]
        )
        
        key_learnings_md = "\n\n".join(
            [f"* **{learning.concept}:** {learning.explanation}" for learning in summary.key_learnings]
        )

        content = SUMMARY_TEMPLATE.format(
            title=summary.title,
            author=summary.author,
            source_file=source_pdf_path.name,
            tags=", ".join(summary.tags),
            high_level_summary=summary.high_level_summary,
            core_themes=core_themes_md,
            key_learnings=key_learnings_md
        )

        with open(output_path, "w", encoding='utf-8') as f:
            f.write(content)
        print(f"    -> Summary saved to: {output_path.name}")

        # Also copy to main Inbox for Knowledge Graph Agent
        shutil.copy(output_path, MAIN_INBOX_DIR / filename)
        print(f"    -> Copied summary to main Inbox for Knowledge Graph Agent: {filename}")

# --- Main Execution ---

if __name__ == "__main__":
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("ERROR: Please set the GEMINI_API_KEY environment variable.")
    else:
        agent = PydanticBookAgent(api_key=api_key)
        agent.run()
