# Retrieval-Augmented Generation (RAG) for Small Language Models (SLMs)

This repository implements a **Retrieval-Augmented Generation (RAG) pipeline** designed to work efficiently with local **Small Language Models (SLMs)** as well as standard language models.

The complete workflow is demonstrated in [rag_demo.ipynb](rag_demo.ipynb).

## 🧠 System Architecture
The system consists of two phases:

### 1. Offline Preparation Phase

Documents are processed once and stored for efficient retrieval:

**PDF file(s)** → [Load](src/document_loader.py) → [Text Chunking](src/chunking.py) → [Text Embedding](src/embedding.py) → [Store in Vector DB (FAISS)](src/vector_store.py)

### 2. Online Inference Phase

User queries are answered using retrieved document context:

**User Query** → [Query Embedding](src/embedding.py) → [Vector Retrieval (FAISS)](src/vector_store.py) → [Prompt Construction (Query + Retrieved Chunks)](src/prompt_constructor.py) → [SLM / LLM](src/lm.py) → **Generated Answer**

## Project Structure

```
$ tree
.
├── rag_demo.ipynb
├── data
│   ├── document.md
│   └── document.pdf
├── requirements.txt
└── src
    ├── chunking.py
    ├── document_loader.py
    ├── embedding.py
    ├── lm.py
    ├── prompt_constructor.py
    └── vector_store.py
```
**Note:** PDF content is extracted into a Markdown (`.md`) file rather than plain text (`.txt`), as Markdown can preserve more structure and be more informative for language models.  
See the example: [data/document.md](data/document.md)

## Setup & Usage

#### 1- Install dependencies

```bash
pip install -r requirements.txt
```

#### 2- Hugging Face authentication

Provide an access token to use **Hugging Face** models.

You may create a token at:
https://huggingface.co/settings/tokens

Then run the following command and enter the token:
```bash
huggingface-cli login
```

#### 3- Run the pipeline
- Place PDF documents in the [data](data/) directory.
- Run the offline indexing pipeline to build the vector database.
- Query the system using the online inference pipeline.