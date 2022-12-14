from rest_framework.decorators import api_view
from rest_framework.generics import (ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView, GenericAPIView)
from rest_framework.response import Response
from rest_framework import  permissions

from .models import Todo, SoftDeleteModel
from .serializers import TodoSerializer
from .permissions import IsOwner

# Create your views here.


@api_view(http_method_names=['GET'])
def status_count(request):
    backlog = Todo.objects.filter(status = 'Backlog').filter(user = request.user).count()
    inprogress = Todo.objects.filter(status = 'In Progress').filter(user = request.user).count()
    finished = Todo.objects.filter(status = 'Finished').filter(user = request.user).count()
    overdue = Todo.objects.filter(status = 'Over Due').filter(user = request.user).count()
    trash = Todo.objects.filter(status = 'Trash').filter(user = request.user).count()
    

    return Response({'backlog': backlog, 'in progress': inprogress, 'finished': finished, 'over due': overdue, 'trash': trash})



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
    
