from fastapi import FastAPI, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import os
import requests
import re
from dotenv import load_dotenv

# Load Together API key from .env file
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

# FastAPI app setup
app = FastAPI()

# CORS setup for Streamlit frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Function to read uploaded file and convert to pandas DataFrame
def read_uploaded_file(file: UploadFile) -> pd.DataFrame:
    filename = file.filename
    content = file.file.read()

    if filename.endswith(".csv"):
        return pd.read_csv(io.BytesIO(content))
    elif filename.endswith(".xlsx") or filename.endswith(".xls"):
        return pd.read_excel(io.BytesIO(content))
    else:
        raise ValueError("Unsupported file format")

# Function to send prompt to Together AI and extract only code
def ask_together(prompt: str) -> str:
    url = "https://api.together.xyz/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",  # ✅ Free serverless model
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.2,
        "max_tokens": 1000
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        content = response.json()["choices"][0]["message"]["content"]

        # Extract only code from markdown-style code blocks
        match = re.search(r"```(?:python)?\s*([\s\S]+?)\s*```", content)
        if match:
            return match.group(1).strip()
        else:
            # If no code block, return raw text (still clean)
            return content.strip()
    else:
        print("❌ Together API Error:", response.status_code, response.text)
        raise Exception("Together API Error: " + response.text)

# Endpoint: Generate Python cleaning code based on user instruction
@app.post("/generate-cleaning-code")
async def generate_cleaning_code(file: UploadFile, instruction: str = Form(...)):
    try:
        df = read_uploaded_file(file)
        preview = df.head(5).to_string()

        prompt = f"""You are a data cleaning assistant. Based on the following user instruction:

\"\"\"{instruction}\"\"\"

And this sample of a pandas DataFrame named `df`:

{preview}

Write Python code that performs appropriate cleaning on the DataFrame `df`.
Don't import anything. Don't explain. Only return valid, executable code.
"""
        code = ask_together(prompt)
        return {"code": code}
    except Exception as e:
        return {"error": str(e)}

# Endpoint: Generate Plotly chart code based on user prompt
@app.post("/generate-chart-code")
async def generate_chart_code(file: UploadFile, prompt: str = Form(...)):
    try:
        df = read_uploaded_file(file)
        preview = df.head(5).to_string()

        full_prompt = f"""You are a data visualization expert. Based on the user request:

\"\"\"{prompt}\"\"\"

And the following sample from a pandas DataFrame `df`:

{preview}

Write a Python code snippet that creates a chart using Plotly (preferably plotly.express).
Assume `df` is already defined. Only return clean chart code, no imports or explanations.
"""
        code = ask_together(full_prompt)
        return {"code": code}
    except Exception as e:
        return {"error": str(e)}
