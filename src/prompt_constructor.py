def construct_prompt(user_query: str, retrieved_chunks: list, embedded_chunks: list):
    """
    Build prompts from retrieved context and user queries.
    """
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