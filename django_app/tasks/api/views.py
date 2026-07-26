from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import filters

from django.shortcuts import get_object_or_404

from tasks.models import Attachment, Task

from .serializers import AttachmentSerializer, CommentSerializer, TaskSerializer


class TaskListAPIView(ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
    ]

    search_fields = [
        'title',
        'description',
    ]

    ordering_fields = [
        'title',
        'created_at',
        'due_date',
    ]
    ordering = ['id']

    def get_queryset(self):
        query_set = Task.objects.filter(owner=self.request.user)

        status = self.request.query_params.get('status')
        priority = self.request.query_params.get('priority')

        if status:
            query_set = query_set.filter(status=status)
        if priority:
            query_set = query_set.filter(priority=priority)

        return query_set

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

class AttachmentListCreateAPIView(ListCreateAPIView):
    serializer_class = AttachmentSerializer
    permission_classes = [IsAuthenticated]

    def get_task(self):
        return get_object_or_404(
            Task,
            pk=self.kwargs['task_pk'],
            owner=self.request.user,
        )

    def get_queryset(self):
        return self.get_task().attachments.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(
            task=self.get_task(),
            uploaded_by=self.request.user,
        )






















