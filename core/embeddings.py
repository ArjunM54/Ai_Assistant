from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)
sentence1 = model.encode("Pyton is amazing")
sentence2 = model.encode("I love coding in python")

#c_s is used to find the similar meaning of the sentences(near to 1 means higher).
score = cosine_similarity([sentence1],[sentence2])
#print(score)
def create_embedding(text):

    embedding = model.encode(text)

    return embedding