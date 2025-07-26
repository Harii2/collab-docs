from django.urls import path
from documents.views import version_views

urlpatterns = [
    path('<int:document_id>/versions/', version_views.get_document_versions, name='get_document_versions'),
    path('<int:document_id>/versions/<int:version_number>/', version_views.get_document_version, name='get_document_version'),
]
