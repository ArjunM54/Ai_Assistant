from reader.pdf_reader import read_pdf
from test_items.text_splitter import split_text
from core.embeddings import create_embedding
from core.vectorsearch import search
from faiss import build_index

text = read_pdf("uploads/computer_networks.pdf")

chunks = split_text(text)

chunk_embeddings = []

for chunk in chunks:
    chunk_embeddings.append(create_embedding(chunk))

index = build_index(chunk_embeddings)

question = input("Ask: ")

query_embedding = create_embedding(question)

compare = search(query_embedding,index,chunks,k=5)

for r in compare:
    print(f"Distance: {r["distance"]:.4f}")
    print(r["chunk"])
    print("=" * 50)

print("\nTop Results:\n")

"""for i, result in enumerate(compare, start=1):
    print("=" * 60)
    print(f"Result {i}")
    print(f"Score : {result['score']:.4f}")
    print(f"Chunk :\n{result['chunk']}")
    print()"""