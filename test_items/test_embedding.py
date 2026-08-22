from core.embeddings import create_embedding

text = "python is amaaaazing!"

emb = create_embedding(text)

print(len(emb))