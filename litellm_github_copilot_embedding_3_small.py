from litellm import embedding

# Example using text-embedding-3-small model via GitHub Copilot
response = embedding(
    model="github_copilot/text-embedding-3-small",
    input=[
        "The quick brown fox jumps over the lazy dog",
        "Machine learning is a subset of artificial intelligence",
        "Python is a versatile programming language"
    ]
)

print("Embedding response:")
print(f"Model: {response.model}")
print(f"Number of embeddings: {len(response.data)}")

# Print details for the first embedding
if response.data:
    first_embedding = response.data[0]
    emb = first_embedding["embedding"] if isinstance(first_embedding, dict) else first_embedding.embedding
    idx = first_embedding.get("index") if isinstance(first_embedding, dict) else getattr(first_embedding, "index", None)
    print(f"First embedding dimensions: {len(emb)}")
    print(f"First few values: {emb[:5]}")
    if idx is not None:
        print(f"Embedding index: {idx}")

# Example with a single text input
single_response = embedding(
    model="github_copilot/text-embedding-3-small",
    input="This is a single text for embedding"
)

print("\nSingle text embedding:")
first = single_response.data[0]
first_emb = first["embedding"] if isinstance(first, dict) else first.embedding
print(f"Embedding dimensions: {len(first_emb)}")
usage = getattr(single_response, "usage", None)
if usage is not None:
    total_tokens = usage.get("total_tokens") if isinstance(usage, dict) else getattr(usage, "total_tokens", None)
    if total_tokens is not None:
        print(f"Usage tokens: {total_tokens}")
