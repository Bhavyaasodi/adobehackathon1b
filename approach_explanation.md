# Round 1B - Approach Explanation

## 🎯 Problem Overview

Given a collection of PDFs, a user persona, and a job-to-be-done (JTBD), the goal is to extract and rank the most relevant sections across the documents that best help the user complete the task.

## 💡 High-Level Solution

The solution performs semantic search and content ranking using Sentence Transformers and cosine similarity. It processes all PDFs, breaks them into chunks, matches them against the persona and job context, and returns ranked sections with metadata in a structured JSON format.

---

## 🛠️ Step-by-Step Methodology

### 1. PDF Text Extraction
- Used **PyMuPDF (fitz)** to extract text from each PDF.
- Text is extracted **page by page** and stored with page numbers.

### 2. Input Handling
- Two text files are used:
  - `persona.txt` → describes the user's role.
  - `job.txt` → describes what the user wants to achieve.
- These inputs are combined into a single query for semantic search.

### 3. Embedding & Semantic Matching
- Used `sentence-transformers` with the model `all-MiniLM-L6-v2` to generate vector embeddings for:
  - Each paragraph or chunk from the PDFs.
  - The combined persona + job query.
- Computed **cosine similarity** between the query and each chunk.

### 4. Section Ranking & Filtering
- Top-matching paragraphs are selected based on similarity score.
- Redundant or similar entries are filtered out.
- Assigned an `importance_rank` based on similarity.

### 5. Sub-section Refinement
- Each selected paragraph is included as `refined_text` with the original page number and source PDF.

### 6. Output Generation
- Final results are saved in `app/output/final_output.json`.
- Output format strictly follows Adobe’s JSON schema.

---

## ✅ Libraries Used

- `PyMuPDF` – PDF parsing
- `sentence-transformers` – contextual embeddings
- `transformers` – backbone utilities
- `torch` – backend for model inference
- `scikit-learn` – cosine similarity

---

## ⚙️ Compliance with Constraints

| Constraint                    | Status      |
|------------------------------|-------------|
| CPU-only Execution           | ✅ Met       |
| Model size < 1 GB            | ✅ Met       |
| Runtime < 60 seconds         | ✅ Met       |
| No internet access needed    | ✅ Met       |

---

## 📌 Summary

The model generalizes well across domains by focusing on semantic similarity, enabling it to work across research, finance, and educational content without domain-specific tuning.

The approach is modular, offline-capable, and follows best practices in zero-shot text matching to ensure adaptability and robustness.
