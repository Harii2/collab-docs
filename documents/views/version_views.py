from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from documents.serializers import DocumentVersionSerializer
from documents.interactors.versions.version_interactor import VersionCrudInteractor


# Initialize interactor (it handles its own storage dependencies internally)
version_interactor = VersionCrudInteractor()


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_document_versions(request, document_id):
    versions = version_interactor.get_document_versions(document_id, request.user.id)
    serializer = DocumentVersionSerializer(versions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_document_version(request, document_id, version_number):
    version = version_interactor.get_version_by_number(document_id, version_number, request.user.id)
    if not version:
        return Response({'error': 'Version not found or access denied'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = DocumentVersionSerializer(version)
    return Response(serializer.data)
