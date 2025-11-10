from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('upload/', views.upload_document, name='upload_document'),
    path('delete/<int:doc_id>/', views.delete_document, name='delete_document'),
    path('chat/', views.new_chat, name='new_chat'),
    path('chat/<int:session_id>/', views.chat_view, name='chat'),
    path('chat/<int:session_id>/send/', views.send_message, name='send_message'),
    path('chat/<int:session_id>/delete/', views.delete_chat, name='delete_chat'),
]