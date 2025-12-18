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