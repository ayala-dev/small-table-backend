from rest_framework import viewsets
from .models import UserRole
from .serializers import UserRoleSerializer
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .permission import IsAdminOrReadOnly


class UserRoleViewSet(viewsets.ModelViewSet):
    queryset = UserRole.objects.all()
    serializer_class = UserRoleSerializer
    permission_classes = [IsAdminOrReadOnly]



