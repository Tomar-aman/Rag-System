from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from .models import Document, ChatSession, ChatMessage
from .rag_service import RAGService
import json

rag_service = RAGService()

def index(request):
    """Main page"""
    documents = Document.objects.all().order_by('-uploaded_at')
    chat_sessions = ChatSession.objects.all().order_by('-created_at')
    return render(request, 'index.html', {
        'documents': documents,
        'chat_sessions': chat_sessions
    })

def upload_document(request):
    """Handle document upload"""
    if request.method == 'POST':
        file = request.FILES.get('document')
        title = request.POST.get('title', file.name)
        
        if file:
            # Save document
            document = Document.objects.create(
                title=title,
                file=file
            )
            
            # Process document
            try:
                num_chunks = rag_service.process_document(document)
                document.processed = True
                document.save()
                messages.success(request, f'Document uploaded and processed! Created {num_chunks} chunks.')
            except Exception as e:
                messages.error(request, f'Error processing document: {str(e)}')
                document.delete()
        
        return redirect('index')
    
    return redirect('index')

def delete_document(request, doc_id):
    """Delete a document"""
    document = get_object_or_404(Document, id=doc_id)
    document.delete()
    messages.success(request, 'Document deleted successfully!')
    return redirect('index')

def chat_view(request, session_id=None):
    """Chat interface"""
    if session_id:
        session = get_object_or_404(ChatSession, id=session_id)
    else:
        session = ChatSession.objects.create(title="New Chat")
        return redirect('chat', session_id=session.id)
    
    messages_list = session.messages.all()
    documents = Document.objects.filter(processed=True)
    
    return render(request, 'chat.html', {
        'session': session,
        'messages': messages_list,
        'documents': documents
    })

@csrf_exempt
def send_message(request, session_id):
    """Handle chat messages"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')
            
            session = get_object_or_404(ChatSession, id=session_id)
            
            # Save user message
            ChatMessage.objects.create(
                session=session,
                role='user',
                content=user_message
            )
            
            # Generate response
            response = rag_service.chat(user_message)
            
            # Save assistant message
            ChatMessage.objects.create(
                session=session,
                role='assistant',
                content=response
            )
            
            return JsonResponse({
                'status': 'success',
                'response': response
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)

def new_chat(request):
    """Create new chat session"""
    session = ChatSession.objects.create(title="New Chat")
    return redirect('chat', session_id=session.id)

def delete_chat(request, session_id):
    """Delete chat session"""
    session = get_object_or_404(ChatSession, id=session_id)
    session.delete()
    return redirect('index')