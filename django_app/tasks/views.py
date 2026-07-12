from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404

from tasks.models import Task, Comment, Attachment
from .forms import TaskForm


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
    # if request.method == "POST":
    #     title = request.POST.get('title')
    #     description = request.POST.get('description')
    #     priority = request.POST.get('priority')
    #     due_date = request.POST.get("due_date") or None
    #
    #     Task.objects.create(
    #         title=title,
    #         description=description,
    #         priority=priority,
    #         owner=request.user,
    #         due_date=due_date,
    #     )
    #     return redirect("task_list")
    # return render(request, "tasks/create_task.html")

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
    # task = get_object_or_404(Task, id=task_id, owner=request.user)
    #
    # if request.method == "POST":
    #     task.title = request.POST.get("title")
    #     task.description = request.POST.get("description")
    #     task.status = request.POST.get("status")
    #     task.priority = request.POST.get("priority")
    #     task.due_date = request.POST.get("due_date") or None
    #     task.save()
    #
    #     return redirect("task_detail", task_id=task_id)
    #
    # return render(request, "tasks/edit_task.html", {"task": task})

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

    if request.method == "POST":
        text = request.POST.get("text")
        uploaded_file = request.FILES.get("file")

        if text:
            Comment.objects.create(
                task=task,
                author=request.user,
                text=text,
            )

        if uploaded_file:
            Attachment.objects.create(
                task=task,
                uploaded_by=request.user,
                file=uploaded_file,
            )

        return redirect("task_detail", task_id=task.id)

    comments = task.comments.order_by("-created_at")
    attachments = task.attachments.order_by("-created_at")

    return render(
        request,
        "tasks/task_detail.html",
        {
            'task': task,
            'comments': comments,
            'attachments': attachments,
        },
    )
