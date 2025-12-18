"""
Prompt constructor take both retrieved chunks and user query and construct the final prompt.

Build a structured prompt such as:

```
You are an assistant.
Answer the question using ONLY the provided context.

Context:
{retrieved_chunks}

Question:
{user_query}
```

Then insert retrieved chunks:

```
You are an assistant.
Answer the question using ONLY the provided context.

Context:
[Chunk 18]
"... Section 4 discussion ..."

[Chunk 19]
"... Further analysis of (part of Section 5) ..."

Question:
What improvement does method A achieve over the baseline?
```
"""