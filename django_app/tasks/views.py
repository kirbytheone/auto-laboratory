from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.http import require_POST

from tasks.models import Task, Comment, Attachment
from .forms import TaskForm, CommentForm, AttachmentForm


@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user)

    status = request.GET.get("status")
    priority = request.GET.get("priority")

    if status:
        tasks = tasks.filter(status=status)

    if priority:
        tasks = tasks.filter(priority=priority)

    tasks = tasks.order_by("-created_at")

    return render(
        request,
        "tasks/task_list.html",
        {
            "tasks": tasks,
            "selected_status": status,
            "selected_priority": priority,
        },
    )

@login_required
def create_task(request):
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            return redirect("task_list")
    else:
        form = TaskForm()

    return render(
        request,
        "tasks/create_task.html",
        {"form": form},
    )

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id,
        owner=request.user,
    )
    if request.method == "POST":
        form = TaskForm(
            request.POST,
            instance=task
        )
        if form.is_valid():
            form.save()
            return redirect("task_detail", task_id=task.id)
    else:
        form = TaskForm(instance=task)

    return render(
        request,
        "tasks/edit_task.html",
        {
            "form": form,
            "task": task
        },
    )

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id,
        owner=request.user,
    )

    if request.method == "POST":
        task.delete()
        return redirect("task_list")

    return render(
        request,
        "tasks/delete_task.html",
        {"task": task},
    )

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id,
        owner=request.user,
    )

    comments = task.comments.order_by("-created_at")
    attachments = task.attachments.order_by("-created_at")

    return render(
        request,
        "tasks/task_detail.html",
        {
            'task': task,
            'comments': comments,
            'attachments': attachments,
            'comment_form': CommentForm(),
            'attachment_form': AttachmentForm(),
        },
    )

@login_required
@require_POST
def add_comment(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id,
        owner=request.user,
    )

    form = CommentForm(request.POST)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.task = task
        comment.author = request.user
        comment.save()
    return redirect("task_detail", task_id=task.pk)

@login_required
@require_POST
def upload_attachment(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id,
        owner=request.user,
    )

    form = AttachmentForm(request.POST, request.FILES)

    if form.is_valid():
        attachment = form.save(commit=False)
        attachment.task = task
        attachment.uploaded_by = request.user
        attachment.save()
    return redirect("task_detail", task_id=task.pk)
