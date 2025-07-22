from heading_ranker import rank_headings

def get_section_content(section_heading, all_lines_on_page, body_font_size):
    """
    Extracts and cleans the text content for a given section, starting from its
    heading line and stopping at the next heading line.
    """
    content_lines = []
    start_index = -1

    # Find the index of our heading line on the page
    for i, line in enumerate(all_lines_on_page):
        if line['bbox'] == section_heading['bbox']:
            start_index = i
            break
            
    if start_index == -1:
        return ""

    # Start with the heading's own text
    content_lines.append(section_heading['text'])

    # Iterate through lines that come *after* the heading line
    for i in range(start_index + 1, len(all_lines_on_page)):
        current_line = all_lines_on_page[i]
        
        # If the current line is identified as a new heading, stop.
        if rank_headings(current_line, body_font_size) is not None:
            break
        
        # --- START OF NEW CLEANING LOGIC ---
        
        text_to_add = current_line['text']
        
        # 1. Replace all known Unicode bullet characters with nothing.
        text_to_add = text_to_add.replace('\uf0b7', '').replace('\u2022', '')
        
        # 2. Strip leading/trailing whitespace to handle indented bullets.
        text_to_add = text_to_add.strip()
        
        # 3. Remove "o " style bullets, which are common in recipes.
        if text_to_add.startswith('o '):
            text_to_add = text_to_add[2:].strip()
        
        # --- END OF NEW CLEANING LOGIC ---

        if text_to_add:
            content_lines.append(text_to_add)
            
    # Join all cleaned lines into a single string.
    # The final ' '.join(final_text.split()) is a robust way to normalize
    # all whitespace (multiple spaces, newlines) into single spaces.
    final_text = " ".join(content_lines)
    return " ".join(final_text.split())


def refine_top_sections(ranked_sections, lines_cache, body_font_sizes, top_k=5):
    """
    For the top-k ranked sections, this function extracts their full text content.
    """
    top = ranked_sections[:top_k]
    refined = []
    
    for section_heading in top:
        doc_name = section_heading['document']
        if doc_name not in lines_cache:
            continue
            
        all_lines_in_doc = lines_cache[doc_name]
        body_font_size = body_font_sizes[doc_name]
        
        # Filter for lines on the same page as the heading
        lines_on_page = [line for line in all_lines_in_doc if line['page'] == section_heading['page']]
        
        context = get_section_content(section_heading, lines_on_page, body_font_size)

        if context:
            refined.append({
                "document": doc_name,
                "page_number": section_heading['page'],
                "refined_text": context
            })
    return refined