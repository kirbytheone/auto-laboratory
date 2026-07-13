from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from tasks.models import Task

from .serializers import CommentSerializer, TaskSerializer


class TaskListAPIView(ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(owner=self.request.user)

class CommentListCreateAPIView(ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_task(self):
        return get_object_or_404(
            Task,
            pk=self.kwargs['task_pk'],
            owner=self.request.user,
        )

    def get_queryset(self):
        task = self.get_task()

        return task.comments.order_by('created_at')

    def perform_create(self, serializer):
        serializer.save(
            task=self.get_task(),
            author=self.request.user,
        )






















