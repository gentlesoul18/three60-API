from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import (
    GenericAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveAPIView,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from three60.utils import status_changer
from .models import Todo
from .serializers import TodoSerializer, CreateTodoSerializer
from .permissions import IsOwner

# Create your views here.


@api_view(http_method_names=["GET"])
@permission_classes((permissions.IsAuthenticated, IsOwner))
def status_count(request):
    todos = Todo.objects.filter(deleted=False)
    backlog = todos.filter(status="Backlog").filter(user=request.user).count()
    inprogress = todos.filter(status="In Progress").filter(user=request.user).count()

    finished = todos.filter(status="Finished").filter(user=request.user).count()
    overdue = todos.filter(status="Over Due").filter(user=request.user).count()
    trash = Todo.objects.filter(status="Trash").filter(user=request.user).count()

    todo_counts = [
        {
            "id": 1,
            "title": "All-Todos",
            "value": todos.filter(user=request.user).count(),
        },
        {"id": 2, "title": "Backlog", "value": backlog},
        {"id": 3, "title": "In-Progress", "value": inprogress},
        {"id": 4, "title": "Finished", "value": finished},
        {"id": 5, "title": "Over-Due", "value": overdue},
        {"id": 6, "title": "Trash", "value": trash},
    ]
    return Response(todo_counts)


class TodoListApi(ListAPIView):
    serializer_class = TodoSerializer
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner,
    )
    queryset = Todo.objects.filter(deleted=False)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class TodoCreateApi(CreateAPIView):
    serializer_class = CreateTodoSerializer
    queryset = Todo.objects.all()
    permission_classes = (
        permissions.IsAuthenticated,
        IsOwner,
    )

    def create(self, request):
        serializer = CreateTodoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=self.request.user)
        return Response(serializer.data)

    def get_queryset(self):
        todo = self.queryset.filter(user=self.request.user)


class TodoDetailApi(RetrieveAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.filter(deleted=False)
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class TodoUpdateApi(GenericAPIView):
    serializer_class = TodoSerializer
    queryset = Todo.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    lookup_field = "id"

    def put(self, request, id):
        obj = self.queryset.get(id=id)
        status = request.data["status"]
        new_status = status_changer(str(status))
        serializer = TodoSerializer(instance=obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["status"] = new_status
        serializer.save(user=self.request.user)
        return Response(serializer.data)
    
    def patch(self, request, id):
        obj = self.queryset.get(id=id)
        status = request.data["status"]
        new_status = status_changer(str(status))
        serializer = TodoSerializer(instance=obj, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data["status"] = new_status
        serializer.save(user=self.request.user)
        return Response(serializer.data)

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class TodoDeleteApi(APIView):
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    queryset = Todo.objects.filter(deleted=False)
    lookup_field = "id"

    def delete(self, request, id):
        todo = self.queryset.get(id=id)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
