# 📚 RAG Document Chat System

A full-stack Django application that enables intelligent conversations with your documents using RAG (Retrieval Augmented Generation) and Google's Gemini AI.

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/Django-5.0-green.svg)

## ✨ Features

- 📄 **Multi-format Support**: Upload PDF, DOCX, and TXT files
- 🤖 **AI-Powered Chat**: Intelligent responses using Google Gemini
- 🔍 **Semantic Search**: Find relevant information using vector embeddings
- 💬 **Multiple Sessions**: Manage different chat conversations
- 💾 **Persistent Storage**: ChromaDB for efficient vector storage
- 🎨 **Modern UI**: Beautiful, responsive interface
- ⚡ **Real-time Chat**: Instant responses with typing indicators

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Upload    │────▶│   Process    │────▶│   Store     │
│  Documents  │     │  & Chunk     │     │  Vectors    │
└─────────────┘     └──────────────┘     └─────────────┘
                                                │
                                                ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Display   │◀────│   Generate   │◀────│  Retrieve   │
│  Response   │     │   (Gemini)   │     │  Relevant   │
└─────────────┘     └──────────────┘     └─────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Git

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/Tomar-aman/Rag-System
cd Rag-System
```

2. **Create virtual environment**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
# Create .env file
cp .env.example .env

# Add your Gemini API key
# Get it from: https://makersuite.google.com/app/apikey or https://aistudio.google.com/app/api-keys
```

Edit `.env`:
```env
GEMINI_API_KEY=your_gemini_api_key_here
```

5. **Create required directories**
```bash
mkdir media templates static chroma_db
```

6. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Create superuser (optional)**
```bash
python manage.py createsuperuser
```

8. **Start the development server**
```bash
python manage.py runserver
```

9. **Open in browser**
```
http://127.0.0.1:8000/
```

## 📖 Usage

### Uploading Documents

1. Navigate to the home page
2. Enter a document title
3. Select a file (PDF, DOCX, or TXT)
4. Click "Upload & Process"
5. Wait for processing to complete

### Chatting with Documents

1. Click "Start New Chat"
2. Type your question in the input box
3. Press Enter or click "Send"
4. View AI-generated responses based on your documents

### Example Questions

- "What is the main topic of this document?"
- "Summarize the key points"
- "Find information about [specific topic]"
- "What does the document say about [subject]?"

## 🛠️ Technology Stack

| Component | Technology |
|-----------|-----------|
| **Backend Framework** | Django 5.0 |
| **AI Model** | Google Gemini 1.5 Flash |
| **Vector Database** | ChromaDB |
| **Embeddings** | Sentence Transformers |
| **Frontend** | HTML, CSS, JavaScript |
| **Document Processing** | PyPDF2, python-docx |

## 📁 Project Structure

```
Rag-System/
├── rag_project/              # Main project directory
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   └── wsgi.py              # WSGI configuration
├── rag_app/                 # Main application
│   ├── models.py           # Database models
│   ├── views.py            # View functions
│   ├── urls.py             # App URL routing
│   ├── rag_service.py      # RAG logic
│   └── admin.py            # Admin configuration
├── templates/               # HTML templates
│   ├── index.html          # Home page
│   └── chat.html           # Chat interface
├── media/                   # Uploaded documents
├── chroma_db/              # Vector database
├── static/                  # Static files
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (create this)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file with the following:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key

```

### Settings Customization

Edit `rag_project/settings.py` to customize:

- Database configuration
- Media file storage
- ChromaDB path
- Chunk size and overlap
- Number of retrieved chunks

## 🎯 How It Works

### 1. Document Processing
- Extracts text from uploaded files
- Splits text into chunks (500 words with 50-word overlap)
- Generates embeddings using Sentence Transformers
- Stores vectors in ChromaDB

### 2. Query Processing
- Converts user query to embedding
- Performs semantic search in ChromaDB
- Retrieves top 3 most relevant chunks

### 3. Response Generation
- Sends relevant chunks + query to Gemini
- Generates contextual response
- Returns answer to user

---

⭐ **If you find this project helpful, please give it a star!** ⭐

Made with ❤️ by Aman Tomar