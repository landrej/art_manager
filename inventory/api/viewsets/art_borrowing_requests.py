from rest_framework import viewsets, status
from rest_framework.response import Response
from inventory.models import ArtBorrowingRequest
from inventory.api.serializers import ArtBorrowingRequestSerializer
import rest_framework.permissions as permissions

class IsAuthor(permissions.DjangoModelPermissions):
    def has_permission(self, request, view):
        if request.method == 'DELETE' and request.user.has_perm('inventory.delete_own_request'):
            return True
        return super().has_permission(request, view)
    def has_object_permission(self, request, view, obj):
        if request.method == 'DELETE' and request.user.has_perm('inventory.delete_own_request') and obj.requester == request.user:
            return True
        return super().has_permission(request, view)

class ArtBorrowingRequestViewSet(viewsets.ModelViewSet):
    queryset = ArtBorrowingRequest.objects.all()
    serializer_class = ArtBorrowingRequestSerializer
    permission_classes = [IsAuthor|permissions.DjangoObjectPermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if 'requester' in serializer.validated_data \
            and serializer.validated_data['requester'] is not None \
            and serializer.validated_data['requester'] != request.user:
            print(serializer.validated_data['requester'])
            print(request.user)
            return Response({'error_message': 'requester can only be the current user'}, status=status.HTTP_400_BAD_REQUEST)
        serializer.validated_data['requester'] = request.user
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
