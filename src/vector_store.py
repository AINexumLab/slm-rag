"""
Create a vector index using FAISS (or similar)

https://github.com/facebookresearch/faiss

Each vector is linked to the original text chunk and metadata.

Save and load the index so don't need to recompute embeddings every time.
"""

"""
The query vector is compared against stored chunk vectors.

Similarity search finds top-K relevant chunks.

Example (K=3):
Chunk 18 (something in Section 5) ← most similar
Chunk 19 (another thing in Section 5)
Chunk 12 (related discussion)
"""

import faiss
import numpy as np

class FaissVectorStore:
    def __init__(self, embedding_dim):
        self.index = faiss.IndexFlatIP(embedding_dim)

    def add(self, embeddings):
        self.index.add(np.array(embeddings).astype("float32"))

    def search(self, query_embedding, top_k=3):
        scores, indices = self.index.search(np.array([query_embedding]).astype("float32"), top_k)

        results = []
        for idx, score in zip(indices[0], scores[0]):
            results.append((idx, float(score)))

        return results