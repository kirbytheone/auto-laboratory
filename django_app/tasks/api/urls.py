from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token

from .views import (
    AttachmentListCreateAPIView,
    CommentListCreateAPIView,
    TaskDetailAPIView,
    TaskListAPIView,
)

urlpatterns = [
    path('schema/', SpectacularAPIView.as_view(), name='api-schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='api-schema'), name='api-docs'),
    path('token/', obtain_auth_token, name='api-token'),
    path('tasks/', TaskListAPIView.as_view(), name='api-task-list'),
    path('tasks/<int:pk>/', TaskDetailAPIView.as_view(), name='api-task-detail'),
    path('tasks/<int:task_pk>/comments/', CommentListCreateAPIView.as_view(), name='api-task-comment-list'),
    path(
        'tasks/<int:task_pk>/attachments/',
        AttachmentListCreateAPIView.as_view(),
        name='api-task-attachment-list'),
]
