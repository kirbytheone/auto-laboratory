from django.urls import path

from .views import CommentListCreateAPIView, TaskListAPIView, TaskDetailAPIView

urlpatterns = [
    path('tasks/', TaskListAPIView.as_view(), name='api-task-list'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='api-task-detail'),
    path('tasks/<int:task_pk>/comments/', CommentListCreateAPIView.as_view(), name='api-task-comment-list'),
]
