from sentence_transformers import SentenceTransformer

model = SentenceTransformer("intfloat/e5-small-v2")
model.save("e5-small-v2-local")
