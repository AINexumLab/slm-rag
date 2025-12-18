# SLM RAG

> [!NOTE]
> Currently, this project is under development. This README file and other source code may contain guidelines for development and will serve as project documentation once it is completed.

Offline Preparation:
``` 
PDF file(s) -> Load -> Chunking -> Embedding -> Store in Vector DB (FAISS)
```

Online Phase:
```
User Query -> Embedding -> Retrieval

Retrieved Text + User Query -> Prompt Construction -> SLM/LLM -> Answer
```