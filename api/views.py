from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from .models import Task, User
from .serializers import TaskSerializer, UserRegisterSerializer, UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated
from .permissions import IsOwnerOrAdmin
from rest_framework.decorators import action
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

# Custom token to include user role
class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['role'] = user.role
        return token

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class RegisterView(generics.CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserRegisterSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        # Short-circuit Swagger schema generation
        if getattr(self, 'swagger_fake_view', False):
            return Task.objects.none()

        user = self.request.user

        # Ensure user is authenticated before accessing role
        if user.is_authenticated and getattr(user, 'role', None) == "admin":
            return Task.objects.all().order_by('-created_at')
        elif user.is_authenticated:
            return Task.objects.filter(owner=user).order_by('-created_at')
        else:
            return Task.objects.none()
