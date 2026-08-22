import numpy as np


def search(query_embedding, index, chunks, k=5):

    query = np.array(
        [query_embedding],
        dtype="float32"
    )

    distances, indices = index.search(query, k)

    results = []

    for distance, idx in zip(distances[0], indices[0]):

        if idx == -1:
            continue

        results.append(
            {
                "chunk": chunks[idx]["text"],
                "source": chunks[idx]["source"],
                "distance": float(distance),
                "index": idx
            }
        )

    return results