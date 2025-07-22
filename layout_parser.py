import fitz  # PyMuPDF
from collections import defaultdict

def extract_lines(pdf_path):
    """
    A robust text extractor that correctly reads text spans with their style
    and merges them into complete, coherent lines, sorted by position.
    """
    doc = fitz.open(pdf_path)
    all_lines = []

    for page_num, page in enumerate(doc, start=1):
        # Using "dict" provides detailed info including font, size, and bbox
        blocks = page.get_text("dict").get("blocks", [])
        spans_by_line = defaultdict(list)

        # 1. Extract all text spans and group them by their vertical baseline
        for block in blocks:
            if "lines" in block:
                for line in block.get("lines", []):
                    for span in line.get("spans", []):
                        # Use the rounded vertical baseline as the key for grouping spans into a line
                        line_key = round(span['bbox'][3])
                        spans_by_line[line_key].append(span)

        # 2. Reconstruct each line from its horizontally sorted spans
        sorted_line_keys = sorted(spans_by_line.keys())
        for line_key in sorted_line_keys:
            spans = sorted(spans_by_line[line_key], key=lambda s: s['bbox'][0])
            line_text = " ".join([s['text'] for s in spans]).strip()
            
            if line_text:
                font_sizes = [s['size'] for s in spans]
                fonts = [s['font'] for s in spans]

                # A line is considered bold if the most common font name in it contains "bold"
                dominant_font = max(fonts, key=fonts.count, default="").lower()
                is_bold = any(style in dominant_font for style in ['bold', 'black', 'heavy'])

                all_lines.append({
                    'text': line_text,
                    'font_size': max(font_sizes) if font_sizes else 0,
                    'is_bold': is_bold,
                    'page': page_num,
                    'bbox': tuple(spans[0]['bbox']) if spans else (0,0,0,0)
                })

    return all_lines