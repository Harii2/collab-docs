from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from documents.serializers import (
    DocumentSerializer, 
    CreateDocumentSerializer, 
    UpdateDocumentSerializer
)
from documents.dtos import CreateDocumentDTO, UpdateDocumentDTO, DocumentListFilterDTO
from interactors.documents.document_crud_interactor import DocumentCrudInteractor
from documents.storage import DocumentStorage, CollaboratorStorage, DocumentVersionStorage


document_storage = DocumentStorage()
collaborator_storage = CollaboratorStorage()
version_storage = DocumentVersionStorage()

document_interactor = DocumentCrudInteractor(document_storage, collaborator_storage, version_storage)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_document(request):
    serializer = CreateDocumentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    dto = CreateDocumentDTO(
        title=serializer.validated_data['title'],
        content=serializer.validated_data['content'],
        owner_id=request.user.id,
        status=serializer.validated_data['status'],
        is_public=serializer.validated_data['is_public']
    )
    
    document = document_interactor.create_document(dto)
    response_serializer = DocumentSerializer(document)
    return Response(response_serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_document(request, document_id):
    document = document_interactor.get_document(document_id, request.user.id)
    if not document:
        return Response({'error': 'Document not found or access denied'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = DocumentSerializer(document)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_document(request, document_id):
    serializer = UpdateDocumentSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    dto = UpdateDocumentDTO(
        id=document_id,
        title=serializer.validated_data.get('title'),
        content=serializer.validated_data.get('content'),
        status=serializer.validated_data.get('status'),
        is_public=serializer.validated_data.get('is_public')
    )
    
    document = document_interactor.update_document(dto, request.user.id)
    if not document:
        return Response({'error': 'Document not found or access denied'}, status=status.HTTP_404_NOT_FOUND)
    
    response_serializer = DocumentSerializer(document)
    return Response(response_serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_document(request, document_id):
    success = document_interactor.delete_document(document_id, request.user.id)
    if not success:
        return Response({'error': 'Document not found or access denied'}, status=status.HTTP_404_NOT_FOUND)
    
    return Response({'message': 'Document deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_documents(request):
    filter_dto = DocumentListFilterDTO(
        owner_id=request.GET.get('owner_id'),
        status=request.GET.get('status'),
        is_public=request.GET.get('is_public') == 'true' if request.GET.get('is_public') else None,
        limit=int(request.GET.get('limit', 20)),
        offset=int(request.GET.get('offset', 0))
    )
    
    documents = document_interactor.list_user_documents(request.user.id, filter_dto)
    serializer = DocumentSerializer(documents, many=True)
    return Response(serializer.data)
