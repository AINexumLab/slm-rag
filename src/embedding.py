"""
Convert (1) each chunk of loaded document or (2) user query into a vector using an embedding model.

The same embedding model will be used in both offline preparation and online phase.

Each chunk, for example, will be:
Chunk 18 -> vector R^768    

Vectors capture semantic meaning, not exact words.
"""

#pip install -U sentence-transformers

# comment below is for my fucking tensorflow issues
"""
import os
os.environ["TRANSFORMERS_NO_TF"] = "1" 
"""


from sentence_transformers import SentenceTransformer

model = SentenceTransformer("BAAI/bge-base-en-v1.5")

def embed_chunks(chunks):
    texts = [f"{c['text']}" for c in chunks]
    embeddings = model.encode(
        texts,
        normalize_embeddings=True,
        batch_size=32,
        show_progress_bar=True,
        convert_to_numpy=True      #Returns embeddings as NumPy arrays
        #convert_to_tensor=True     #Returns a PyTorch tensor
        #device="cpu"
    )

    for chunk, emb in zip(chunks, embeddings):
        chunk["embedding"] = emb

    return chunks

def embed_query(query: str):
    # Based on https://huggingface.co/BAAI/bge-base-en-v1.5
    instruction = "Represent this sentence for searching relevant passages:"
    
    embedding = model.encode(
        f"{instruction} {query}",
        normalize_embeddings=True,
        convert_to_numpy=True
    )
    
    return embedding