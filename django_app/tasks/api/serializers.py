from rest_framework import serializers

from tasks.models import Attachment, Comment, Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id',
            'title',
            'description',
            'status',
            'priority',
            'due_date',
            'created_at',
            'updated_at',
        ]

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(
        source='author.username',
        read_only=True,
    )

    class Meta:
        model = Comment
        fields = [
            'id',
            'text',
            'author',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'author',
            'created_at',
        ]

class AttachmentSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.CharField(
        source='uploaded_by.username',
        read_only=True,
    )

    class Meta:
        model = Attachment

        fields = [
            'id',
            'filename',
            'file',
            'uploaded_by',
            'created_at',
        ]

        read_only_fields = [
            'id',
            'filename',
            'uploaded_by',
            'created_at',
        ]
