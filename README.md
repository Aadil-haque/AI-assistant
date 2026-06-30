# AI-assistant
# ResourcePlus AI Assistant

An AI-powered chatbot built for the ResourcePlus employee platform. The assistant uses Retrieval-Augmented Generation (RAG) to answer employee queries from company documentation while maintaining conversation history and providing a modern chat interface.

---

## Features

- AI-powered employee assistant
- Retrieval-Augmented Generation (RAG)
- ChromaDB vector database
- FastAPI backend
- React + Vite frontend
- Conversation history using SQLite
- Automatic conversation title generation
- Markdown response rendering
- Voice input support
- Responsive modern UI
- Collapsible conversation sidebar

---

## Tech Stack

### Backend

- Python 3.11+
- FastAPI
- LangChain
- ChromaDB
- Sentence Transformers
- SQLite

### Frontend

- React
- Vite
- Axios
- Framer Motion
- React Markdown
- Lucide React

---

## Project Structure

```
chatbot/
│
├── backend/
│   ├── api/
│   ├── database/
│   └── rag/
│
├── crawler/
│   ├── data/
│   ├── docs/
│   └── output/
│
├── frontend/
│   └── AI-assistant/
│
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/<repository>.git
cd chatbot
```

---

### 2. Create a virtual environment

```bash
python -m venv venv
```

Windows

```bash
venv\Scripts\activate
```

Linux / macOS

```bash
source venv/bin/activate
```

---

### 3. Install backend dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Install frontend dependencies

```bash
cd frontend/AI-assistant
npm install
```

---

## Running the Application

### Start Backend

From the project root:

```bash
uvicorn backend.api.search_query:app --reload
```

Backend runs on

```
http://localhost:8000
```

---

### Start Frontend

```bash
cd frontend/AI-assistant
npm run dev
```

Frontend runs on

```
http://localhost:5173
```

---

## Building the Knowledge Base

1. Crawl documentation

```bash
python crawler/scrape_articles.py
```

2. Build embeddings

```bash
python crawler/build_knowledge_base.py
```

This creates the Chroma vector database used by the chatbot.

---

## API Endpoints

### Ask a Question

```
POST /ask
```

Returns an AI-generated response using RAG.

---

### Get Chat History

```
GET /history
```

Returns saved conversations.

---

### Start New Chat

```
POST /new-chat
```

Creates a new conversation session.

---

## Architecture

```
Employee Question
        │
        ▼
 React Frontend
        │
        ▼
 FastAPI Backend
        │
        ▼
Query Processing
        │
        ▼
Vector Search (ChromaDB)
        │
        ▼
Relevant Documents
        │
        ▼
LLM Response Generation
        │
        ▼
Response + Chat History
```

---

## Screenshots

Add screenshots of:

- Home screen
- Chat interface
- Sidebar
- AI response
- Mobile view (optional)

---

## Future Improvements

- User authentication
- Multi-user support
- Streaming AI responses
- File upload support
- Admin analytics dashboard
- OCR support for documents
- Better conversation search

---

## Author

**Aadil Haque**

Computer Engineering Student

Internship Project – AI Assistant for ResourcePlus

---

## License

This project was developed as part of an internship assignment and is intended for educational and demonstration purposes.
