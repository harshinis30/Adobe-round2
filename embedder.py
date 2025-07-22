from sentence_transformers import SentenceTransformer

# Initialize the model once and reuse it.
# "intfloat/e5-small-v2" is a good, lightweight model for this task.
model = SentenceTransformer("intfloat/e5-small-v2")

def encode_texts(texts):
    """
    Encodes a list of texts into sentence embeddings.
    """
    return model.encode(texts, convert_to_tensor=True)