from django.urls import path, include

urlpatterns = [
    path('', include('documents.urls.document_urls')),
    path('', include('documents.urls.collaborator_urls')),
    path('', include('documents.urls.version_urls')),
]
