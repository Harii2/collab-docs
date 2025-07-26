from django.urls import path
from documents.views import collaborator_views

urlpatterns = [
    path('<int:document_id>/collaborators/', collaborator_views.get_document_collaborators, name='get_document_collaborators'),
    path('<int:document_id>/collaborators/add/', collaborator_views.add_collaborator, name='add_collaborator'),
    path('<int:document_id>/collaborators/<int:user_id>/update/', collaborator_views.update_collaborator, name='update_collaborator'),
    path('<int:document_id>/collaborators/<int:user_id>/remove/', collaborator_views.remove_collaborator, name='remove_collaborator'),
]
