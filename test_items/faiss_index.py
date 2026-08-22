import faiss
import numpy as np

def build_index(chunk_embeddings):

    embeddings = np.array(chunk_embeddings, dtype=np.float32)

    print("Embeddings Shape:", embeddings.shape)

    if embeddings.ndim != 2:
        raise ValueError(
            f"Expected 2D embeddings, got shape {embeddings.shape}"
        )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    return index