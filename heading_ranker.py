from collections import Counter

def rank_headings(line, body_font_size):
    """
    Scores an individual line to determine if it's a heading using detailed
    style information.
    """
    score = 0
    text = line['text']
    lower_text = text.lower()

    # --- Strict Filters ---
    # A heading must be a single, non-empty line.
    if not text or '\n' in text:
        return None

    # Filter out common non-title keywords
    if 'ingredients' in lower_text or 'instructions' in lower_text:
        return None
        
    # Filter out lines that are likely list items
    bullet_prefixes = ['o ', '·', '*', '-', '•']
    if any(lower_text.startswith(p) for p in bullet_prefixes):
        return None
    if len(text) > 2 and text[0].isdigit() and text[1] == '.':
        return None

    # --- Scoring Heuristics ---
    # 1. Font Size: A larger font size is a strong indicator.
    if line['font_size'] > body_font_size:
        score += (line['font_size'] - body_font_size) * 1.5

    # 2. Boldness: Being bold is a very strong signal for a heading.
    if line['is_bold']:
        score += 5

    # 3. Capitalization: ALL CAPS or Title Case are good indicators.
    if len(text) > 3 and text.isupper():
        score += 3
    elif text.istitle():
        score += 2
        
    # --- Penalties for non-heading characteristics ---
    # Long lines or lines ending in a period are less likely to be titles.
    if len(text) > 80:
        score -= 4
    if text.endswith('.'):
        score -= 2

    # A line must have a positive score to be considered a heading.
    if score > 2:
        return {
            "text": text,
            "level": "H2" if score > 7 else "H3", # Simple level assignment based on score
            "page": line['page'],
            "bbox": line['bbox']
        }
    return None