from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required

from .models import Task
from .forms import TaskForm


def show_tasks(request: HttpRequest):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})


def show_task(request: HttpRequest, pk: int) -> HttpResponse:
    task = get_object_or_404(Task, pk=pk)
    return render(request, 'tasks/task_detail.html', {'task': task})


@login_required
def create_task(request: HttpRequest):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect("task_detail", pk=task.pk)
    else:
        form = TaskForm()
    return render(request, 'tasks/task_form.html', {'form': form})


def update_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect("task_detail", pk=task.id)
    else:
        form = TaskForm(instance=task)
    return render(request, 'tasks/task_form.html', {'task': task, 'form': form})


def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    if request.method == 'POST':
        task.delete()
        return redirect("task_list")
    return render(request, 'tasks/task_delete.html', {'task': task})


@login_required
@require_POST
@csrf_exempt
def mark_task_as_done(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.is_done = True
    task.save()
    return JsonResponse({'done': True})
