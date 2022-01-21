from multiprocessing import context
from unicodedata import category
from django.shortcuts import render, get_object_or_404, redirect
from .models import Author, Category, Post
from .utils import update_views
from .forms import PostForm
from django.contrib.auth.decorators import login_required


def home(request):
    forums = Category.objects.all()
    context = {
        "forums": forums
    }
    return render(request, "home.html", context)

def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    context = {
        "post":post,
    }
    update_views(request, post)
    return render(request, "detail.html", context)

def posts(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(approved = True, categories = category)

    context = {
        "posts":posts,
        "forum":category,
    }

    return render(request, "posts.html", context)


@login_required
def create_post(request):
    context = {}
    form = PostForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            print("\n\n Nieprawidłowe")
            author = Author.objects.get(user=request.user)
            new_post = form.save(commit=False)
            new_post.user = author
            new_post.save()
            return redirect("home")
    context.update({
        "form": form,
        "title": "Create New Post"
    })
    return render(request, "create_post.html", context)
