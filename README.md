# 📘 PDF Persona-Aware Section Extractor — Hackathon Submission (Round 1B)

### Challenge Theme: *Connect What Matters — For the User Who Matters*

This solution intelligently extracts the **most relevant sections** from a set of PDFs by understanding both the **persona** and the **task to be done** — capturing critical information in a structured, ranked, and summarized JSON format.

---

## 🧠 Approach

Our solution blends **layout parsing**, **heading detection**, **semantic similarity**, and **refined summarization** to locate the most important content — entirely offline.

### 🧩 Key Components

#### 1. **Layout Parsing & Block Metadata**
- Extracts all styled lines from PDFs using `PyMuPDF`, capturing:
  - Font size, boldness, positioning
  - Page-level metadata

#### 2. **Heading Detection via Scoring**
- Scores each line to detect whether it’s a heading using heuristics like:
  - Font size > average body
  - Title casing / short length / boldness
  - Starts at top-left
  - No end punctuation

#### 3. **Intent Embedding**
- Combines persona + job-to-be-done into a single **semantic vector** using `sentence-transformers` (E5-small-v2).
- Generalizes to all domains — academic, finance, education, etc.

#### 4. **Section Relevance Matching**
- Computes **cosine similarity** between all detected headings and the intent vector.
- Top-matching headings are extracted.

#### 5. **Subsection Summarization**
- Lines under top headings are cleaned, dedented, and summarized without losing structure.

---

## 📂 Folder Structure

```
.
├── main.py                  # Entry script: coordinates pipeline
├── layout_parser.py         # Extracts styled lines from PDF
├── heading_ranker.py        # Scores lines for heading likelihood
├── intent_extractor.py      # Converts persona + job to vector
├── section_ranker.py        # Scores headings vs intent
├── summarizer.py            # Extracts content under top headings
├── embedder.py              # Loads and manages sentence transformer
├── Challenge_1b/
│   └── Collection 1/
│       ├── PDFs/            # Input PDFs
│       ├── challenge1b_input.json
│       └── challenge1b_output.json (optional)
├── requirements.txt
├── Dockerfile
├── output.json
└── README.md
```

---

## 📥 Input Format

```json
{
  "persona": { "role": "Travel Blogger" },
  "job_to_be_done": { "task": "Create a travel guide on South of France" },
  "documents": [
    { "filename": "South of France - Cuisine.pdf" },
    { "filename": "South of France - Cities.pdf" }
  ]
}
```

---

## 📤 Output Format

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
      "refined_text": "Bouillabaisse is a traditional stew made with..."
    }
  ]
}
```

---

## 🔧 Build & Run Instructions

Your solution will be tested using:

### ✅ Build Docker Image

```bash
docker build -t persona-extractor .
```

### ▶️ Run Docker Container

```bash
docker run --rm ^
  -v "C:\Users\Larika\Round 2\Challenge_1b\Collection 1\PDFs":/app/input ^
  -v "C:\Users\Larika\Round 2\output":/app/output ^
  --network none persona-extractor
```

---

## ⚙️ Constraints Handled

| Constraint                  | Satisfied? |
|----------------------------|------------|
| ≤ 60s for 5 PDFs           | ✅         |
| CPU-only (amd64)           | ✅         |
| Model ≤ 1 GB               | ✅ (e5-small-v2) |
| No internet access         | ✅         |

---

## ✨ Highlights

* ✅ Semantic understanding of user intent
* 📚 Works across diverse document domains
* 🧠 Combines layout and embedding knowledge
* 🔍 Modular and fully explainable pipeline

---

## 🔒 Notes

* ❌ No hardcoding or file-specific hacks used
* ❌ No internet access needed (all offline)
* ✅ Reusable for future phases (e.g., webapp integration)

---

## 📜 License

MIT License — Free for research and competition use.

---

## 👩‍💻 Authors

Built by R.K.Larika and S.Harshini for the Adobe “Connect the Dots” Hackathon Challenge (Round 1B).
