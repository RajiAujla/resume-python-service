# FastAPI Resume Generator (LaTeX)

This project exposes a FastAPI endpoint that generates a professional resume in LaTeX format using a Hugging Face model.

## Run locally

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Architecture

The Resume Generator has two main components:

1. **FastAPI Python Service** – Accepts user input (name, experience, skills, education) and calls the AI model to generate LaTeX.
2. **Hugging Face Model (Text2Text Generator)** – Generates LaTeX content based on the input.

The flow:

User Input (JSON)
|
v
+-----------------+
| FastAPI Service |
+-----------------+
|
v
+-------------------+
| Hugging Face Model |
+-------------------+
|
v
Generated LaTeX Resume
|
v
User
