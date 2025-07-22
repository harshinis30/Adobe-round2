from sklearn.metrics.pairwise import cosine_similarity
from embedder import encode_texts

def rank_sections(intent_embedding, headings):
    """
    Ranks a list of headings based on their cosine similarity to the user's intent vector.
    """
    if not headings:
        return []
        
    section_texts = [h['text'] for h in headings]
    section_embeddings = encode_texts(section_texts)
    
    # Calculate similarity between the intent and all section headings
    similarities = cosine_similarity(
        intent_embedding.reshape(1, -1),
        section_embeddings
    )[0]
    
    # Combine headings with their scores
    ranked = [
        {**headings[i], "score": float(similarities[i])}
        for i in range(len(headings))
    ]
    
    # Sort by score in descending order
    ranked.sort(key=lambda x: x['score'], reverse=True)
    return ranked