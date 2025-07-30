# 🚀 AI-Powered Data Dashboard Generator

Welcome to **AI Dashboard Generator** — an intelligent app built with **Streamlit + FastAPI** that lets you upload datasets (CSV/Excel), clean them with AI suggestions, and generate stunning visual dashboards, all powered by **Together AI** models.

---

## 📁 Project Structure

```
├── app.py                  # Streamlit frontend
├── api_server.py          # FastAPI backend
├── start.sh               # Shell script to run both servers
├── requirements.txt       # Python dependencies
├── render.yaml            # Render deployment config
├── .env                   # API keys (keep secret)
├── runtime.txt            # Python version (for Render)
├── helpers/
│   ├── ai_api_handler.py
│   ├── dashboard.py
│   ├── file_handler.py
│   ├── insights.py
│   └── utils.py
```

---

## 🧠 Features

- 📤 Upload CSV or Excel datasets  
- 🧼 AI-powered data cleaning suggestions  
- 📊 Auto-generated dashboards using natural language  
- 💬 Chatbot to interact and request custom charts  
- ⚡ Fast backend with FastAPI + Together AI  
- 🎨 Interactive frontend with Streamlit  

---

## 💻 Local Setup (Development)

### 1. 📦 Install Python

Make sure you have **Python 3.10** installed:

```bash
python --version
```

---

### 2. 🧪 Set up virtual environment

```bash
python -m venv venv
source venv/bin/activate       # Linux/macOS
venv\Scripts\activate          # Windows
```

---

### 3. 🔧 Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. 🔑 Add `.env` file

In the root directory, create a `.env` file:

```env
TOGETHER_API_KEY=your_api_key_here
```

---

## 🧪 Run Locally

### 1. Start FastAPI backend

```bash
uvicorn api_server:app --reload
```

### 2. Start Streamlit frontend

In a **new terminal**, run:

```bash
streamlit run app.py
```

---

## 🌍 Deploy on Render

Deploy both frontend and backend together using Render's free tier.

---

### ✅ Prerequisites

Push your project to GitHub and make sure these files exist:

- `start.sh`
- `render.yaml`
- `runtime.txt`
- `.env` (locally only — don't push this to GitHub)

---

### 🛠 `start.sh`

```bash
#!/bin/bash

uvicorn api_server:app --host 0.0.0.0 --port 8000 &
streamlit run app.py --server.port 10000
```

> ✅ Make it executable before commit:

```bash
chmod +x start.sh
```

---

### 🧾 `render.yaml`

```yaml
services:
  - type: web
    name: ai-dashboard-gen
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: ./start.sh
    region: oregon
```

---

### 🐍 `runtime.txt`

```
python-3.10.13
```

---

### ☁️ Deploy Steps

1. Visit 👉 [https://render.com](https://render.com)
2. Click **New > Web Service**
3. Connect your **GitHub repo**
4. If not auto-detected:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `./start.sh`
5. Add environment variable:
   - `TOGETHER_API_KEY=your_api_key_here`
6. Click **Deploy** 🚀

---

## 🛡️ Security

- Never push `.env` to GitHub
- Add it to `.gitignore`:

```
.env
```

---

## 🔧 Tech Stack

| Layer      | Tech                 |
|------------|----------------------|
| Frontend   | Streamlit            |
| Backend    | FastAPI              |
| LLM API    | Together AI (Mistral)|
| Deployment | Render (Free Tier)   |
| Data       | pandas, matplotlib   |

---

## 🙌 Author

Made with ❤️ by **[Mayank Saini](https://github.com/MayankxSaini)**

---

## ⭐ Support

If this project helped you, please give it a ⭐ on GitHub and share it with others!
