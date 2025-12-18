"""
Create a vector index using FAISS (or similar)

https://github.com/facebookresearch/faiss

Each vector is linked to the original text chunk and metadata.

Save and load the index so don't need to recompute embeddings every time.
"""