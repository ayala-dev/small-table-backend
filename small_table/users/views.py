# views.py
from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import User
from .serializers import UserSerializer
from .permission import IsOwnerOrAdmin

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ['username', 'email', 'date_joined', 'is_staff']
    search_fields = ['username', 'email', 'phone']

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]  # הרשאה ליצירת משתמש חדש
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]  # עדכון/מחיקה רק למי שמחובר ומנהל או בעל החשבון
        return [IsAuthenticated()]  # כל לשנות
