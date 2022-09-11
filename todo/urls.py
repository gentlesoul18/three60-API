from django.urls import path
from .views import TodoListApi, TodoCreateApi,TodoDetailApi, TodoUpdateApi, TodoDeleteApi
urlpatterns = [
    path('', TodoListApi.as_view(), name='list'),
    path('create/', TodoCreateApi.as_view(), name= 'create'),
    path('<int:id>', TodoDetailApi.as_view(), name='detail'),
    path('edit/<int:id>', TodoUpdateApi.as_view(), name='update'),
    path('delete/<int:id>', TodoDeleteApi.as_view(), name='delete'),
]

