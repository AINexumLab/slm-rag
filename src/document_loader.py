"""
Input: PDF document(s)

Process:
- Extract raw text (page by page, for example)
- Remove headers, footers, page numbers 

Output: Clean text string
""" 

from pathlib import Path

'''
import pdfplumber
import re
from collections import Counter


def extract_pdf_text(
    pdf_path: str,
    header_footer_threshold: float = 0.6
):

    pages_text = []
    raw_pages = []

    # Extract raw text page by page
    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            lines = text.splitlines()

            raw_pages.append({
                "page_number": page_num,
                "lines": lines
            })

    # Detect repeated headers & footers
    header_candidates = []
    footer_candidates = []

    for page in raw_pages:
        if len(page["lines"]) >= 3:
            header_candidates.append(page["lines"][0])
            footer_candidates.append(page["lines"][-1])

    header_counts = Counter(header_candidates)
    footer_counts = Counter(footer_candidates)

    page_count = len(raw_pages)

    common_headers = {
        text for text, count in header_counts.items()
        if count / page_count >= header_footer_threshold
    }

    common_footers = {
        text for text, count in footer_counts.items()
        if count / page_count >= header_footer_threshold
    }

    # Clean each page
    for page in raw_pages:
        cleaned_lines = []

        for line in page["lines"]:
            line = line.strip()

            # Remove empty lines
            if not line:
                continue

            # Remove detected headers/footers
            if line in common_headers or line in common_footers:
                continue

            # Remove page numbers (e.g. "12", "Page 12", "- 12 -")
            if re.fullmatch(r"(page\s*)?\d+|-\s*\d+\s*-", line.lower()):
                continue

            cleaned_lines.append(line)

        page_text = " ".join(cleaned_lines)
        pages_text.append(page_text)

    # Final clean text
    clean_text = "\n\n".join(pages_text)

    metadata = {
        "source": pdf_path,
        "total_pages": page_count,
        "removed_headers": list(common_headers),
        "removed_footers": list(common_footers),
    }

    return clean_text, metadata
'''


#gemini
'''
import pdfplumber
from collections import Counter

def extract_with_frequency_filter(pdf_path, threshold=0.7):
    with pdfplumber.open(pdf_path) as pdf:
        all_pages_text = []
        potential_headers = []

        # Step 1: Collect first/last lines to find repeats
        for page in pdf.pages:
            lines = page.extract_text().split('\n')
            if len(lines) > 2:
                potential_headers.append(lines[0])  # Top line
                potential_headers.append(lines[-1]) # Bottom line

        # Step 2: Identify strings that repeat on 'threshold' % of pages
        line_counts = Counter(potential_headers)
        to_remove = {line for line, count in line_counts.items() 
                     if count > len(pdf.pages) * threshold}

        # Step 3: Extract and filter
        clean_content = []
        for page in pdf.pages:
            page_text = page.extract_text().split('\n')
            # Remove the line if it's in our "to_remove" list
            filtered_lines = [l for l in page_text if l not in to_remove]
            clean_content.append("\n".join(filtered_lines))

    return "\n\n".join(clean_content)
'''

from pymupdf4llm import to_markdown
from typing import List, Dict

"""
    Load a PDF using PyMuPDF4LLM and return page-level text records.

    Returns a list of:
    {
        "text": str,
        "metadata": {
            "source": str,
            "page_number": int,
            "chunk_index": None,
            "section_title": None
        }
    }
"""

def load_pdf_document(pdf_path: str, output_path: str) -> List[Dict]:
    pages = to_markdown(
        pdf_path,
        page_chunks=True,     # keep page boundaries
        write_images=False    # ignore images for RAG
    )

    documents = []

    for page in pages:
        text = page.get("text", "").strip()

        # Skip empty / junk pages
        if not text:
            continue

        documents.append({
            "text": text,
            "metadata": {
                "source": pdf_path,
                "page_number": None,
                "chunk_index": None,     # filled in chunking.py
                "section_title": None    # can be inferred later
            }
        })

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        for i, page in enumerate(pages, start=1):
            # print(page["text"])
            # print(page["metadata"])
            f.write(f"## Page {i}\n\n")
            f.write(page["text"])
            f.write("\n\n")

    return documents