"""
Prompt constructor take both retrieved chunks and user query and construct the final prompt.

Build a structured prompt such as:

```
You are an assistant.
Answer the question using ONLY the provided context.
The answer should be direct and compact.

Context:
{retrieved_chunks}

Question:
{user_query}
```

Then insert retrieved chunks:

```
You are an assistant.
Answer the question using ONLY the provided context.
The answer should be direct and compact.

Context:
[Chunk 18]
"... Section 4 discussion ..."

[Chunk 19]
"... Further analysis of (part of Section 5) ..."

Question:
What improvement does method A achieve over the baseline?
```
"""

def construct_prompt(user_query: str, retrieved_chunks: list, embedded_chunks: list):
    context = "".join(
        f"[Chunk {index}]\n{embedded_chunks[index]['text']}\n\n"
        for index, _ in retrieved_chunks
    )

    return f"""
You are an assistant.
Answer the question using ONLY the provided context.
The answer should be direct and compact.

Context:
{context}

Question:
{user_query}
"""