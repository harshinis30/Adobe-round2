import os
import json
import argparse
import datetime
from collections import Counter
from layout_parser import extract_lines
from heading_ranker import rank_headings
from intent_extractor import extract_intent_embedding
from section_ranker import rank_sections
from summarizer import refine_top_sections

def analyze_documents(pdf_paths, persona, job):
    all_headings = []
    lines_cache = {}
    body_font_sizes = {}

    print("Step 1: Parsing PDF layouts into structured lines...")
    for path in pdf_paths:
        try:
            doc_name = os.path.basename(path)
            lines = extract_lines(path)
            lines_cache[doc_name] = lines

            # Determine the most common font size to use as the 'body' text size
            if lines:
                font_counts = Counter(round(line['font_size']) for line in lines)
                body_font_sizes[doc_name] = font_counts.most_common(1)[0][0]
            else:
                body_font_sizes[doc_name] = 10 # Default fallback
            
            # Identify headings in the document
            for line in lines:
                heading = rank_headings(line, body_font_sizes[doc_name])
                if heading:
                    heading['document'] = doc_name
                    all_headings.append(heading)
        except Exception as e:
            print(f"⚠️ Warning: Could not process {os.path.basename(path)}. Error: {e}")
    
    print(f"   - Found {len(all_headings)} potential headings across all documents.")

    print("Step 2: Ranking headings based on user intent...")
    intent_embedding = extract_intent_embedding(persona, job)
    ranked_sections = rank_sections(intent_embedding, all_headings)
    
    print("Step 3: Refining content from top-ranked sections...")
    final_summaries = refine_top_sections(ranked_sections, lines_cache, body_font_sizes, top_k=5)
    
    # Format the top sections for the final output
    top_5_sections = ranked_sections[:5]
    formatted_sections = [{
            "document": s['document'],
            "section_title": s['text'],
            "importance_rank": i + 1,
            "page_number": s['page']
        } for i, s in enumerate(top_5_sections)]

    # Assemble the final result
    return {
        "metadata": {
            "input_documents": [os.path.basename(p) for p in pdf_paths],
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.datetime.now().isoformat(),
        },
        "extracted_sections": formatted_sections,
        "subsection_analysis": final_summaries
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyze PDF documents based on user intent.")
    parser.add_argument("--pdf_folder", required=True, help="Path to the folder containing PDF files")
    parser.add_argument("--input_json", required=True, help="Path to the input JSON with persona and job details")
    parser.add_argument("--output", default="output.json", help="Path to save the output JSON file")
    args = parser.parse_args()

    try:
        with open(args.input_json, "r", encoding="utf-8") as f:
            config = json.load(f)
        
        persona = config.get("persona", {}).get("role", "")
        job = config.get("job_to_be_done", {}).get("task", "")
        documents = config.get("documents", [])

        if not documents:
             raise ValueError("No documents found in the input JSON file.")

        pdf_paths = [os.path.join(args.pdf_folder, doc["filename"]) for doc in documents]
        result = analyze_documents(pdf_paths, persona, job)
        
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)
        
        print(f"🎉 Analysis complete. Output saved to {args.output}")

    except Exception as e:
        print(f"❌ An unexpected error occurred: {e}")