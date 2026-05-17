from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from tasks.models import Task


@login_required
def task_list(request):
    tasks = Task.objects.filter(owner=request.user).order_by("-created_at")

    return render(
        request,
        "tasks/task_list.html",
        {"tasks": tasks},
    )

@login_required
def create_task(request):
    if request.method == "POST":
        title = request.POST.get('title')
        description = request.POST.get('description')
        priority = request.POST.get('priority')

        Task.objects.create(
            title=title,
            description=description,
            priority=priority,
            owner=request.user,
        )
        return redirect("task_list")
    return render(request, "tasks/create_task.html")

@login_required
def task_detail(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id,
        owner=request.user,
    )

    return render(
        request,
        "tasks/task_detail.html",
        {'task': task},
    )
