# 🤖 SentinoMind AI — Automated AI News & Facebook Publisher

SentinoMind AI is a fully automated AI-powered content pipeline that fetches real-time news from the internet, processes and enriches it using multiple AI models, generates matching images, stores everything in Supabase, and automatically publishes posts to a Facebook Page — all with minimal human intervention.

---

## 🚀 Features

- 🌐 **Real-time News Fetching** — Searches Google News across multiple categories using Serper API
- 🧠 **AI Content Processing** — Analyzes and generates viral social media posts using Groq (Llama models)
- 🎨 **AI Image Generation** — Generates cinematic, metaphorical images using HuggingFace FLUX, Pollinations, Together AI, and Fal.ai as fallbacks
- 🛡️ **Safety Pipeline** — Automatically audits and refines prompts for safety before image generation
- 💾 **Cloud Storage** — Stores all content and images in Supabase database and storage
- 📲 **Facebook Auto-Publishing** — Posts content directly to Facebook Pages via Graph API
- 🖥️ **Streamlit Dashboard** — Clean UI to monitor, review, and manage all generated content

---

## 🏗️ Architecture
```
Internet (Google News via Serper API)
        ↓
   NewsFetcher — fetches & stores raw news
        ↓
   PostCreator — AI analyzes & generates post content (Groq)
        ↓
   ImageGenerator — generates & validates images (HF/Pollinations/Together/Fal)
        ↓
   Supabase DB & Storage
        ↓
   Streamlit UI — review generated content
        ↓
   FastAPI Backend — posts to Facebook via Graph API
```

---

## 📁 Project Structure
```
SentinoMind AI/
├── Backend/
│   ├── engine.py          # FastAPI backend
│   └── main.py            # AI pipeline runner
├── content_engine/
│   ├── news_fetcher.py    # Fetches news from internet
│   ├── post_creator.py    # AI content generation
│   └── image_gen.py       # AI image generation
├── db_management/
│   └── supabase_handler.py # Database operations
├── root_folder/
│   └── interface.py       # Streamlit UI
├── .env.example           # Environment variables template
├── requirements.txt       # Python dependencies
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/mdarifminhaz79/SentinoMind-AI-.git
cd SentinoMind-AI-
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Copy `.env.example` to `.env` and fill in your API keys:
```bash
cp .env.example .env
```

### 5. Run the backend
```bash
cd Backend
uvicorn engine:app --reload
```

### 6. Run the Streamlit UI
```bash
streamlit run root_folder/interface.py
```

---

## 🔑 Required API Keys

| Service | Purpose | Get it at |
|---------|---------|-----------|
| Supabase URL & Key | Database & Storage | supabase.com |
| Groq API Key | AI content & image prompts | console.groq.com |
| HuggingFace API Key | Image generation | huggingface.co |
| Google AI Key | AI processing | aistudio.google.com |
| Serper API Key | Google News search | serper.dev |
| Together AI Key | Image generation fallback | api.together.xyz |
| Facebook Page ID | Target Facebook Page | Facebook Developer Console |
| Facebook Page Token | Posting permissions | Facebook Developer Console |

---

## 📊 Content Pipeline Status Flow
```
raw → ready → final → Published
```

| Status | Meaning |
|--------|---------|
| `raw` | News fetched, not yet processed |
| `ready` | AI post content generated |
| `final` | Image generated, ready to post |
| `Published` | Successfully posted to Facebook |

---

## 🛠️ Tech Stack

- **Backend:** FastAPI, Python
- **Frontend:** Streamlit
- **Database:** Supabase (PostgreSQL)
- **Storage:** Supabase Storage
- **AI Models:** Groq (Llama 3.1, 3.3), HuggingFace FLUX, Google GenAI
- **Image Generation:** HuggingFace, Pollinations, Together AI, Fal.ai
- **News Source:** Serper API (Google News)
- **Social Media:** Facebook Graph API v22.0

---

## 📝 License

This project is licensed under the MIT License.
