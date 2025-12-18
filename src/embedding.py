"""
Convert (1) each chunk of loaded document or (2) user query into a vector using an embedding model.

The same embedding model will be used in both offline preparation and online phase.

Each chunk, for example, will be:
Chunk 18 -> vector R^768    

Vectors capture semantic meaning, not exact words.
"""