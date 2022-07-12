"""
These view functions and classes implement API endpoints
"""
from django.shortcuts import render, redirect
from blog.models import BlogPost
from taggit.models import Tag
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import NewUserForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Permission
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.contenttypes.models import ContentType


def index(request):
    """
    Blog home page
    """
    posts = BlogPost.objects.all()
    tags = Tag.objects.all()
    print(posts)
    context = {'posts': posts, 'tags': tags}
    return render(request, 'blog/home.html', context)


def blog_post(request, slug):
    """
    Single blog post view
    """
    post = BlogPost.objects.get(slug=slug)
    tags = Tag.objects.all()
    context = {'post': post, 'tags': tags}
    return render(request, 'blog/post.html', context)


def user_register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_staff = True
            content_type = ContentType.objects.get_for_model(BlogPost)
            post_permissions = Permission.objects.filter(content_type=content_type)
            user.user_permissions.set(post_permissions)
            user.save()
            messages.success(request, "Registration successful.")
            return redirect('login')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = NewUserForm()
    return render(request=request, template_name="blog/register.html",
                  context={"register_form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return HttpResponseRedirect(reverse('admin:index'))
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request=request, template_name="blog/login.html", context={"login_form": form})



