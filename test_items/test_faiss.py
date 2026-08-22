import numpy as np
from test_items.faiss_index import build_index
from core.embeddings import create_embedding

texts = [
    "I love python",
    "Artificial intelligence",
    "cloud computing",
    "Machine learning"
]

embeddings = []
for i in texts:
    embeddings.append(create_embedding(i))

index = build_index(embeddings)

print(index.ntotal)