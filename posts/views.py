from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpRequest

from .models import Post, User
from .forms import PostForm


def show_posts(request):
    posts = Post.objects.all()
    return render(request, 'posts/post_list.html', {'posts': posts})


def show_post(request: HttpRequest, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'posts/post_detail.html', {'post': post})


def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})
