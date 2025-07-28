from sentence_transformers import SentenceTransformer

# Load the model from the local folder directly
model = SentenceTransformer("e5-small-v2-local")

def encode_texts(texts):
    """
    Encodes a list of texts into sentence embeddings.
    """
    return model.encode(texts, convert_to_tensor=True)
