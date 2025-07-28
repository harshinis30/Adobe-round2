# 📘 PDF Outline Extractor — Hackathon Submission (Round 1A)

### Challenge Theme: *Connecting the Dots Through Docs*

This solution extracts a structured outline from any PDF — including the document **title**, and all **H1, H2, H3** headings — in a clean, multilingual-aware, hierarchical JSON format.

---

## 🧠 Approach

Our approach combines **layout heuristics**, **font size clustering**, and **score-based heading detection** to understand the structure of any PDF like a machine would.

### 🧩 Key Components:

#### 1. **Layout-Aware Block Extraction**
- Uses [`PyMuPDF`](https://github.com/pymupdf/PyMuPDF) to extract text spans with font size, position, and style metadata.
- Constructs paragraph blocks per line for heading analysis.

#### 2. **Font Size Clustering**
We extract all unique font sizes and assign:
- Largest → `H1`
- Second Largest → `H2`
- Third Largest → `H3`

This dynamic strategy adjusts to variations in font across documents.

```python
# cluster_font_sizes
font_sizes = sorted(set(font_sizes), reverse=True)
size_map = {"H1": font_sizes[0], "H2": font_sizes[1], "H3": font_sizes[2]}
```

#### 3. **Heading Scoring & Anomaly Filtering**

Each block is scored based on:

* Font size relative to average
* Boldness, uppercase ratio
* Short length (likely heading)
* Top-of-page / left alignment
* Absence of trailing punctuation
* Matches multilingual section patterns like `1.1`, `A.2`, `一.二` using Unicode-aware regex

Only high-scoring blocks are treated as heading candidates.

#### 4. **Multilingual Support**

* Our regex captures multilingual numbering (e.g., Japanese, Hindi, Chinese).
* Unicode ranges are used for:

  * Arabic: `\u0600–\u06FF`
  * CJK: `\u4E00–\u9FFF`
* Easily extensible to other scripts.

---

## 📂 Folder Structure

```
.
├── main.py                  # Pipeline entry point
├── layout_parser.py         # Extracts text spans from PDF
├── heading_ranker.py        # Scores heading blocks using heuristics
├── utils.py                 # Font size clustering + level mapping
├── output/                  # Output JSON directory
├── input/                   # Input PDF directory
├── Dockerfile               # Submission-ready Dockerfile
├── README.md                # This file
```

---

## 📦 Libraries Used

| Library             | Purpose                                  |
| ------------------- | ---------------------------------------- |
| `PyMuPDF`           | PDF text and layout parsing (`fitz`)     |
| `re`                | Regex matching for multilingual headings |
| `json`, `sys`, `os` | File I/O and orchestration               |

No deep learning. No web calls. Fully offline.

---

## 🔧 Build & Run Instructions

⚠️ Your solution will be run using the *Expected Execution* below — make sure your local testing mirrors this.

### ✅ Build the Docker image

```bash
docker build --platform linux/amd64 -t mysolutionname:somerandomid .
```

### ▶️ Run the Docker container

```bash
docker run --rm \
  -v $(pwd)/input:/app/input \
  -v $(pwd)/output:/app/output \
  --network none \
  mysolutionname:somerandomid
```

### 🧾 What It Does

* Reads all PDFs in `/app/input`
* Writes corresponding `filename.json` files into `/app/output`
* Output format:

```json
{
  "title": "Understanding AI",
  "outline": [
    { "level": "H1", "text": "Introduction", "page": 1 },
    { "level": "H2", "text": "What is AI?", "page": 2 },
    { "level": "H3", "text": "History of AI", "page": 3 }
  ]
}
```

---

## ⚙️ Constraints Handled

| Constraint            | Handled?          |
| --------------------- | ----------------- |
| ≤ 10s per 50-page PDF | ✅                 |
| Model size ≤ 200MB    | ✅ (no model used) |
| No internet           | ✅                 |
| CPU-only (amd64)      | ✅                 |

---

## 🧪 Testing Guide (Locally)

1. Put any `.pdf` files inside the `input/` folder.
2. Run the docker container.
3. Check the corresponding `.json` outputs inside `output/`.

---

## ✨ Highlights

* ✅ Purely rule-based: fast and explainable
* 🧠 Intelligent: position, font, and boldness awareness
* 🌍 Multilingual-aware: supports Hindi, Chinese, Arabic, Japanese patterns
* ⚡️ Efficient: fully offline, no dependencies larger than PyMuPDF

---

## 🔒 Notes

* ❌ No hardcoding or file-specific hacks used
* ❌ No external model downloads or APIs
* ✅ Modular and ready to extend for Round 1B

---

## 📜 License

MIT License — free for research and hackathon use.

---

## 👩‍💻 Author

Made by R.K.Larika and S.Harshini — developed as part of the “Understand Your Document” hackathon challenge.
