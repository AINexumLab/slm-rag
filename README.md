# SLM RAG

Offline Preparation:
``` 
PDF file(s) -> Load -> Chunking -> Embedding -> Store in Vector DB (FAISS)
```

Online Phase:
```
User Query -> Embedding -> Retrieval

Retrieved Text + User Query -> Prompt Construction -> SLM/LLM -> Answer
```