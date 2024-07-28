from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from django.utils.text import slugify
from django.views.decorators.http import require_POST
from django.db.models import Q
from django.contrib import messages

from .models import Post
from .forms import PostForm


def get_post_list(request):
    q_filter = Q(is_published=True) if not request.user.has_perm('blog.publish_post') else Q()
    posts = Post.objects.select_related('author').filter(q_filter).all()
    return render(request, 'blog/post_list.html', context={
        "posts": posts,
    })


def get_post_detail(request, slug):
    qs = Post.objects.select_related('author').all()
    if not request.user.is_authenticated:
        qs = qs.filter(is_published=True)
    post = get_object_or_404(qs, slug=slug)
    return render(request, 'blog/post_detail.html', context={
        "post": post,
    })


@permission_required('blog.add_post')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.slug = slugify(form.cleaned_data['title'])
            post.save()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog/post_form.html', context={
        "form": form,
    })


@login_required
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        messages.warning(request, 'Only the author can edit this post.')
        return redirect('blog:post_detail', slug=post.slug)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save()
            return redirect('blog:post_detail', slug=post.slug)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_form.html', context={
        "post": post,
        "form": form,
    })


@login_required
def remove_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if post.author != request.user:
        messages.warning(request, 'Only the author can remove this post.')
        return redirect('blog:post_detail', slug=post.slug)
    if request.method == 'POST':
        post.delete()
        return redirect('blog:post_list')
    return render(request, 'blog/post_confirm_delete.html', context={
        "post": post,
    })


@require_POST
@permission_required('blog.publish_post')
def publish_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.is_published = True
    post.save()
    messages.success(request, 'Post published successfully.')
    return redirect('blog:post_detail', slug=post.slug)
