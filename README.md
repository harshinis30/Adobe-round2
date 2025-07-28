
# 📚 PDF Intent-Based Section Extractor

This project processes collections of PDF documents to extract and summarize the most relevant sections based on a **persona** and a **task**. It combines layout parsing, heading identification, semantic similarity ranking, and content summarization to deliver focused insights.

---

## 🚀 Overview

Given:
- A **persona** (e.g., Travel Blogger)
- A **job-to-be-done** (e.g., Create a guide on South of France)
- A **set of PDF documents** (e.g., travel information)

The system:
1. Parses the layout and structure of each PDF.
2. Detects headings using font and formatting heuristics.
3. Matches headings with the user’s intent using sentence embeddings.
4. Extracts and refines relevant content under those headings.

---

## 🗂️ Project Structure

```
ROUND_2/
├── Challenge_1b/
│   └── Collection 1/
│       ├── PDFs/                         # PDF files for analysis
│       ├── challenge1b_input.json        # Input with persona and job
│       └── challenge1b_output.json       # Sample or generated output
├── embedder.py                           # Embedding utility using Sentence Transformers
├── heading_ranker.py                     # Scores lines to detect headings
├── intent_extractor.py                   # Converts persona + task to embedding
├── layout_parser.py                      # Extracts styled lines from PDFs
├── main.py                               # Main pipeline controller
├── output.json                           # Output after execution
├── requirements.txt                      # Required Python libraries
├── section_ranker.py                     # Matches headings with intent
├── summarizer.py                         # Extracts text under top-ranked headings
└── .gitignore                            # Excludes cache, virtual env, etc.
```

---

## 📥 Input Format

The input should be a JSON file like this:

```json
{
  "persona": { "role": "Travel Blogger" },
  "job_to_be_done": { "task": "Find content for travel guide on South of France" },
  "documents": [
    { "filename": "South of France - Cities.pdf" },
    { "filename": "South of France - Cuisine.pdf" }
  ]
}
```

---

## ⚙️ Setup

### 1. Clone the Repository
```bash
git clone <repo-url>
cd ROUND_2
```

### 2. Create Virtual Environment (Optional)
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Requirements
```bash
pip install -r requirements.txt
```

---

## ▶️ Running the Project

```bash
python main.py \
  --pdf_folder "Challenge_1b/Collection 1/PDFs" \
  --input_json "Challenge_1b/Collection 1/challenge1b_input.json" \
  --output "output.json"
```

---

## 🔍 How It Works

### 📄 1. `layout_parser.py`
Uses `PyMuPDF` to extract lines of text with metadata like font size, font name, boldness, and position.

### 🧠 2. `heading_ranker.py`
Applies heuristics to decide whether a line is a heading:
- Font size > body size
- Bold or title-case formatting
- Not a bullet or overly long line

### ✨ 3. `intent_extractor.py`
Encodes persona + job into a sentence embedding using the `intfloat/e5-small-v2` transformer.

### 🧮 4. `section_ranker.py`
Uses cosine similarity to score all headings against the intent embedding and rank them.

### 🧹 5. `summarizer.py`
Extracts lines under each top heading, removes bullet characters and extra whitespace, and returns cleaned text.

---

## 📤 Output Format

The output is a JSON like:

```json
{
  "metadata": {
    "input_documents": [...],
    "persona": "...",
    "job_to_be_done": "...",
    "processing_timestamp": "..."
  },
  "extracted_sections": [
    {
      "document": "South of France - Cuisine.pdf",
      "section_title": "Local Dishes",
      "importance_rank": 1,
      "page_number": 2
    }
  ],
  "subsection_analysis": [
    {
      "document": "South of France - Cuisine.pdf",
      "page_number": 2,
      "refined_text": "Local Dishes Bouillabaisse is a traditional Provençal stew..."
    }
  ]
}
```

---

## 🧩 Dependencies

Major libraries used:
- `sentence-transformers`
- `scikit-learn`
- `PyMuPDF`
- `torch`
- `transformers`

Install them with:
```bash
pip install -r requirements.txt
```

---

## 📌 Notes

- Designed for structured, well-formatted PDFs (e.g., reports, guides).
- Uses layout, not OCR.
- Adaptable to various use cases like travel, food, history, and more.

---

## 👩‍💻 Authors

Built with ❤️ for semantic PDF analysis using NLP and layout heuristics.
