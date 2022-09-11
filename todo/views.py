from ast import Delete
from re import U
from rest_framework.generics import (ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView)
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import serializers, status, permissions
from drf_yasg.utils import swagger_auto_schema
from three60.mixins import UpdateModelMixin, ApiAuthMixin
from .models import Todo
from .serializers import TodoSerializer
from .permissions import IsOwner

# Create your views here.


class TodoListApi(ListAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsOwner,)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class TodoCreateApi(CreateAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsOwner,)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class TodoDetailApi(RetrieveAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class TodoUpdateApi(UpdateAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

class TodoDeleteApi(DestroyAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner,)
    lookup_field = "id"

    