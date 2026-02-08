import faiss
import numpy as np

class FaissVectorStore:
    """
    https://github.com/facebookresearch/faiss
    """
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