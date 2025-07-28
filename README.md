# Adobe India Hackathon 2025 - Round 1B Submission

## 📌 Problem

Extract and rank relevant sections from PDFs based on persona and job-to-be-done.

---

## 🚀 How to Run (via Docker)

```bash
docker build --platform linux/amd64 -t adobe-hackathon-1b .
docker run --rm -v $(pwd)/app/input:/app/input -v $(pwd)/app/output:/app/output --network none adobe-hackathon-1b
