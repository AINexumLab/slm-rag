"""
Split text into chunks.

Have to define:
Chunk size (e.g., 300 tokens)
Overlap (e.g., 50 tokens)
   
Sample: 
```
Chunk 17:
"... Section 4 discussion ..."

Chunk 18:
"... Section 5 Method A improves accuracy by ..."

Chunk 19:
"... Further analysis of (part of Section 5) ..."
```

Each chunk has text and metadata (e.g., document_id, section number, page number)
"""

# pip install -U langchain-text-splitters

# from langchain.text_splitter import RecursiveCharacterTextSplitter
# from langchain.text_splitter import MarkdownHeaderTextSplitter


import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(md_path: str):
    with open(md_path, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    pages = re.split(r"\n## Page \d+\n", markdown_text)
    pages = [p.strip() for p in pages if p.strip()]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
        is_separator_regex=False, #separators=["\n\n", "\n", ".", " ", ""]
        length_function=len,
    )

    results = []
    chunk_index = 0

    for page_number, page_text in enumerate(pages, start=1):
        chunks = splitter.split_text(page_text)

        for chunk in chunks:
            results.append({
                "text": chunk,
                "metadata": {
                    "source": md_path,
                    "page_number": page_number,
                    "chunk_index": chunk_index,
                }
            })
            chunk_index += 1

    return results
