from django.db.models import Count, Q
from rest_framework.generics import (ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView)
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework import serializers, status, permissions
from drf_yasg.utils import swagger_auto_schema
from todo.softdelete import SoftDeleteModel
from .models import Todo
from .serializers import TodoSerializer, TodoStatusCountSerializer
from .permissions import IsOwner

# Create your views here.
class TodoStatusCountApi(ListAPIView):
    serializer_class = TodoStatusCountSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner,)

    def get_queryset(self):
        return Todo.objects.annotate(
            nBacklog=Count('pk', filter=Q(status='Backlog')),
            nInProgress=Count('pk', filter=Q(status='In Progress')),
            nFinished=Count('pk', filter=Q(status='Finished')),
            nOverDue=Count('pk', filter=Q(status='Over due')),
            nTrash=Count('pk', filter=Q(status='Trash'))
            ).filter(user = self.request.user)

class TodoListApi(ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = (permissions.IsAuthenticated,IsOwner,)
    queryset = Todo.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user = self.request.user)


class TodoCreateApi(CreateAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = (permissions.IsAuthenticated,IsOwner,)

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
    def get_queryset(self):
        todo =  self.queryset.filter(user=self.request.user)


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
    
