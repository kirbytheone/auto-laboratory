from django.contrib import admin
from tasks.models import Task, Comment

# Register your models here.
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "status",
        "priority",
        "owner",
        "created_at",
    )

    last_filter = (
        "status",
        "priority",
    )

    search_fields = (
        "title",
        "description",
    )

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("id", "task", "author", "created_at")
    search_fields = ("task", "task__title", "author__username")