from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from documents.serializers import (
    CollaboratorSerializer,
    AddCollaboratorSerializer,
    UpdateCollaboratorSerializer
)
from documents.dtos import AddCollaboratorDTO
from interactors.documents.collaborator_crud_interactor import CollaboratorCrudInteractor
from documents.storage import DocumentStorage, CollaboratorStorage


document_storage = DocumentStorage()
collaborator_storage = CollaboratorStorage()

collaborator_interactor = CollaboratorCrudInteractor(document_storage, collaborator_storage)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_collaborator(request, document_id):
    serializer = AddCollaboratorSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    dto = AddCollaboratorDTO(
        document_id=document_id,
        user_id=serializer.validated_data['user_id'],
        permission=serializer.validated_data['permission'],
        added_by_user_id=request.user.id
    )
    
    collaborator = collaborator_interactor.add_collaborator(dto, request.user.id)
    if not collaborator:
        return Response({'error': 'Cannot add collaborator'}, status=status.HTTP_400_BAD_REQUEST)
    
    response_serializer = CollaboratorSerializer(collaborator)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_collaborator(request, document_id, user_id):
    serializer = UpdateCollaboratorSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    collaborator = collaborator_interactor.update_collaborator_permission(
        document_id, user_id, serializer.validated_data['permission'], request.user.id
    )
    if not collaborator:
        return Response({'error': 'Cannot update collaborator'}, status=status.HTTP_404_NOT_FOUND)
    
    response_serializer = CollaboratorSerializer(collaborator)
    return Response(response_serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_collaborator(request, document_id, user_id):
    success = collaborator_interactor.remove_collaborator(document_id, user_id, request.user.id)
    if not success:
        return Response({'error': 'Cannot remove collaborator'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({'message': 'Collaborator removed successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_document_collaborators(request, document_id):
    collaborators = collaborator_interactor.get_document_collaborators(document_id, request.user.id)
    serializer = CollaboratorSerializer(collaborators, many=True)
    return Response(serializer.data)
