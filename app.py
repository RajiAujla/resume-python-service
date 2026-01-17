from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

class ResumeRequest(BaseModel):
    name: str
    experience: str  # comma-separated experience items
    skills: list[str]
    education: str = "Not provided"

# Initialize Hugging Face text2text generator
generator = pipeline("text2text-generation", model="google/flan-t5-base")

@app.post("/generate")
def generate_resume(request: ResumeRequest):
    # --- Generate LaTeX Summary with the model ---
    summary_prompt = (
        f"Write a concise LaTeX summary for {request.name} who has {request.experience} "
        f"and skills {', '.join(request.skills)}. Only output LaTeX code."
    )
    summary = generator(summary_prompt, max_new_tokens=150)[0]['generated_text'].strip()

    # --- Format Experience as proper LaTeX items ---
    # Split experience by comma and create \item for each
    experience_items = [f"\\item {item.strip()}" for item in request.experience.split(",")]
    experience_latex = "\n".join(experience_items)

    # --- Format Skills as proper LaTeX items ---
    skills_items = [f"\\item {skill.strip()}" for skill in request.skills]
    skills_latex = "\n".join(skills_items)

    # --- Assemble full LaTeX document ---
    latex_resume = f"""
\\documentclass{{article}}
\\begin{{document}}

\\section*{{Summary}}
{summary}

\\section*{{Experience}}
\\begin{{itemize}}
{experience_latex}
\\end{{itemize}}

\\section*{{Skills}}
\\begin{{itemize}}
{skills_latex}
\\end{{itemize}}

\\section*{{Education}}
{request.education}

\\end{{document}}
"""
    return {"latex": latex_resume}
