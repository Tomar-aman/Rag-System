import os
import google.generativeai as genai
from PyPDF2 import PdfReader
from docx import Document as DocxDocument
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer
from django.conf import settings

class RAGService:
    def __init__(self):
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('models/gemini-flash-latest')
        
        self.chroma_client = chromadb.PersistentClient(
            path=str(settings.CHROMA_DB_PATH)
        )
        self.collection = self.chroma_client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )
        
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def extract_text_from_pdf(self, file_path):
        """Extract text from PDF file"""
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    def extract_text_from_docx(self, file_path):
        """Extract text from DOCX file"""
        doc = DocxDocument(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def extract_text_from_txt(self, file_path):
        """Extract text from TXT file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    def chunk_text(self, text, chunk_size=500, overlap=50):
        """Split text into chunks with overlap"""
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size - overlap):
            chunk = ' '.join(words[i:i + chunk_size])
            chunks.append(chunk)
        return chunks
    
    def process_document(self, document):
        """Process and index a document"""
        file_path = document.file.path
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            text = self.extract_text_from_pdf(file_path)
        elif file_ext == '.docx':
            text = self.extract_text_from_docx(file_path)
        elif file_ext == '.txt':
            text = self.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_ext}")
  
        chunks = self.chunk_text(text)
        
        for i, chunk in enumerate(chunks):
            embedding = self.embedding_model.encode(chunk).tolist()
            self.collection.add(
                embeddings=[embedding],
                documents=[chunk],
                ids=[f"doc_{document.id}_chunk_{i}"],
                metadatas=[{
                    "document_id": document.id,
                    "document_title": document.title,
                    "chunk_index": i
                }]
            )
        
        return len(chunks)
    
    def retrieve_relevant_chunks(self, query, n_results=3):
        """Retrieve relevant document chunks for a query"""
        query_embedding = self.embedding_model.encode(query).tolist()
  
        collection_count = self.collection.count()
        
        actual_n_results = min(n_results, collection_count) if collection_count > 0 else 1
        
        if collection_count == 0:
            return []
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=actual_n_results
        )
        
        return results['documents'][0] if results['documents'] else []
    
    def generate_response(self, query, context_chunks):
        """Generate response using Gemini with context"""
        context = "\n\n".join(context_chunks)
        
        prompt = f"""You are a helpful assistant that answers questions based on the provided context.

Context from documents:
{context}

Question: {query}

Please provide a detailed answer based on the context above. If the context doesn't contain enough information to answer the question, say so clearly."""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    def chat(self, query):
        """Main chat function - retrieve and generate"""

        relevant_chunks = self.retrieve_relevant_chunks(query, n_results=3)
        
        if not relevant_chunks:
            return "I don't have any documents to reference. Please upload some documents first."
        
        response = self.generate_response(query, relevant_chunks)
        return response