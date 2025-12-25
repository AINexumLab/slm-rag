"""
Input: PDF document(s)

Process:
- Extract raw text (page by page, for example)
- Remove headers, footers, page numbers 

Output: Clean text string
""" 

from pathlib import Path
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




'''
# i could use this here instead of re in next stage
from langchain_core.documents import Document
def to_langchain_documents(pages):
    documents = []

    for page in pages:
        documents.append(
            Document(
                page_content=page["text"],
                metadata=page["metadata"]
            )
        )

    return documents
'''