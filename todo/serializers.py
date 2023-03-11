from rest_framework import serializers
from .models import Todo

class CreateTodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id", "title", "description", "status", "created"]
        extra_kwargs = {
            'status':{'read_only':True}
        }
        

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ["id", "title", "description", "status", "created", "updated"]



    