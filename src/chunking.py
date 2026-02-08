import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(md_path: str):
    with open(md_path, "r", encoding="utf-8") as f:
        markdown_text = f.read()

    pages = re.split(r"\n## Page \d+\n", markdown_text)
    pages = [p.strip() for p in pages if p.strip()]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=600,
        chunk_overlap=25,
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
                    #"section_title": None  this is available in document_loader but removed in this step
                }
            })
            chunk_index += 1

    return results