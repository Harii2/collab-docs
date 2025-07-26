from django.urls import path
from documents.views import document_views

urlpatterns = [
    path('', document_views.list_documents, name='list_documents'),
    path('create/', document_views.create_document, name='create_document'),
    path('<int:document_id>/', document_views.get_document, name='get_document'),
    path('<int:document_id>/update/', document_views.update_document, name='update_document'),
    path('<int:document_id>/delete/', document_views.delete_document, name='delete_document'),
]
