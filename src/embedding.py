from sentence_transformers import SentenceTransformer
import torch

class Embedder:
    """
    Generate vector embeddings for text and query.
    """
    def __init__(self, model_name="BAAI/bge-base-en-v1.5"):
        self.model = SentenceTransformer(model_name)
        print(f"Model: {model_name}")
        
        self.device = "mps" if torch.backends.mps.is_available() else "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Device: {self.device}")

    def embed_query(self, text: str):
        # Based on https://huggingface.co/BAAI/bge-base-en-v1.5 documentation.
        # Instruction is `optional` for this model.
        instruction = "Represent this sentence for searching relevant passages:"
        
        embedding = self.model.encode(
            f"{instruction} {text}",
            normalize_embeddings=True,
            convert_to_numpy=True,
            device=self.device
        )
        
        return embedding
    
    def embed_chunks(self, chunks):
        texts = [c['text'] for c in chunks]
        
        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            batch_size=32,
            show_progress_bar=True,
            device=self.device,
            convert_to_numpy=True      # Returns embeddings as NumPy arrays
            # convert_to_tensor=True   # Returns a PyTorch tensor
        )

        for chunk, emb in zip(chunks, embeddings):
            chunk["embedding"] = emb

        return chunks