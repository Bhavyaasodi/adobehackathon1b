import os
import json
import fitz  # PyMuPDF
from datetime import datetime
from sentence_transformers import SentenceTransformer, util

# Load the model once
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

def read_text_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        return file.read().strip()

def extract_chunks_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    chunks = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        blocks = page.get_text("blocks")
        for block in blocks:
            text = block[4].strip()
            if len(text) >= 40 and not text.startswith("•"):
                chunks.append({
                    "document": os.path.basename(pdf_path),
                    "page_number": page_num + 1,
                    "text": text
                })
    return chunks

def rank_chunks(chunks, persona, job, top_n=5, threshold=0.6):
    query = f"{persona}. Task: {job}"
    query_embedding = model.encode(query, convert_to_tensor=True)
    
    results = []
    for chunk in chunks:
        chunk_embedding = model.encode(chunk["text"], convert_to_tensor=True)
        similarity = util.pytorch_cos_sim(query_embedding, chunk_embedding).item()
        if similarity >= threshold:
            results.append({**chunk, "score": similarity})

    # Sort by descending similarity score
    results = sorted(results, key=lambda x: x["score"], reverse=True)
    return results[:top_n]

def generate_output_json(all_chunks, persona, job, input_docs):
    ranked = rank_chunks(all_chunks, persona, job)

    extracted_sections = []
    subsection_analysis = []

    for i, chunk in enumerate(ranked):
        extracted_sections.append({
            "document": chunk["document"],
            "section_title": chunk["text"][:80],
            "importance_rank": i + 1,
            "page_number": chunk["page_number"]
        })
        subsection_analysis.append({
            "document": chunk["document"],
            "refined_text": chunk["text"],
            "page_number": chunk["page_number"]
        })

    output = {
        "metadata": {
            "input_documents": input_docs,
            "persona": persona,
            "job_to_be_done": job,
            "processing_timestamp": datetime.now().isoformat()
        },
        "extracted_sections": extracted_sections,
        "subsection_analysis": subsection_analysis
    }

    return output

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    input_dir = os.path.join(base_dir, "input")
    output_dir = os.path.join(base_dir, "output")
    os.makedirs(output_dir, exist_ok=True)

    persona_path = os.path.join(base_dir, "persona.txt")
    job_path = os.path.join(base_dir, "job.txt")

    persona = read_text_file(persona_path)
    job = read_text_file(job_path)

    all_chunks = []
    input_documents = []

    for filename in os.listdir(input_dir):
        if filename.endswith(".pdf"):
            input_documents.append(filename)
            pdf_path = os.path.join(input_dir, filename)
            chunks = extract_chunks_from_pdf(pdf_path)
            all_chunks.extend(chunks)

    output_json = generate_output_json(all_chunks, persona, job, input_documents)

    output_path = os.path.join(output_dir, "final_output.json")
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(output_json, f, indent=2, ensure_ascii=False)

    print("✅ Output written to:", output_path)

if __name__ == "__main__":
    main()
