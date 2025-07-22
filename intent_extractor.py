from embedder import encode_texts

def extract_intent_embedding(persona, job):
    """
    Creates an embedding that represents the user's intent.
    """
    prompt = f"Persona: {persona}. Task: {job}"
    # The prompt is encoded into a vector that captures the semantic meaning of the task.
    return encode_texts([prompt])[0]