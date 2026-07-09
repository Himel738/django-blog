import django
from django.shortcuts import get_object_or_404, redirect, render
from blogs.models import Category, Blog
from django.contrib.auth.decorators import login_required,permission_required
from .forms import AddUserForm, BlogPostForm, CategoryForm, EditUserForm
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
@login_required(login_url='login')
def dashboard(request):
    category_count = Category.objects.all().count()
    blogs_count = Blog.objects.all().count()
    context = {
        "category_count": category_count,
        "blogs_count": blogs_count,
    }
    return render(request, "dashboard/dashboard.html", context)

def categories(request):
    categories = Category.objects.all()
    context = {
        "categories": categories,
    }
    return render(request, "dashboard/categories.html", context)

@login_required
def add_category(request):
    if not request.user.has_perm('blogs.add_category'):
        messages.warning(request, "You are not eligible to add a category.")
        return redirect('categories')

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Category added successfully.")
            return redirect('categories')
    else:
        form = CategoryForm()

    context = {
        "form": form,
    }
    return render(request, "dashboard/add_category.html", context)

@login_required
def edit_category(request, pk):
    if not request.user.has_perm('blogs.change_category'):
        messages.warning(request, "You are not eligible to edit this category.")
        return redirect('categories')

    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            messages.success(request, "Category updated successfully.")
            return redirect('categories')
    else:
        form = CategoryForm(instance=category)

    context = {
        "form": form,
        "category": category,
    }
    return render(request, "dashboard/edit_category.html", context)

@login_required
def delete_category(request, pk):
    if not request.user.has_perm('blogs.delete_category'):
        messages.warning(request, "You are not eligible to delete this category.")
        return redirect('categories')

    category = get_object_or_404(Category, pk=pk)
    category.delete()

    messages.success(request, "Category deleted successfully.")
    return redirect('categories')

@login_required
def posts(request):
    if request.user.is_superuser or request.user.has_perm('blogs.view_blog'):
        posts = Blog.objects.all()
    else:
        posts = Blog.objects.filter(author=request.user)

    context = {
        "posts": posts,
    }
    return render(request, "dashboard/posts.html", context)

@login_required
def add_post(request):
    if not request.user.has_perm('blogs.add_blog'):
        messages.warning(request, "You are not eligible to add a post.")
        return redirect('posts')

    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # Temporarily save without committing
            post.author = request.user      # Set the current user as the author
            post.save()                     # Save to get the ID

            title = form.cleaned_data['title']
            post.slug = slugify(title) + '-' + str(post.id)
            post.save()

            messages.success(request, "Post added successfully.")
            return redirect('posts')
    else:
        form = BlogPostForm()

    context = {
        "form": form,
    }
    return render(request, "dashboard/add_post.html", context)
@login_required
def edit_post(request, pk):
    if not request.user.has_perm('blogs.change_blog'):
        messages.warning(request, "You are not eligible to edit this post.")
        return redirect('posts')
    post = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            post = form.save()
            title = form.cleaned_data['title'] 
            post.slug = slugify(title) + '-' + str(post.id)
            post.save()

            messages.success(request, "Post updated successfully.")
            return redirect('posts')
    form = BlogPostForm(instance=post)
    context = {
        "form": form,
        "post": post,
    }
    return render(request, "dashboard/edit_post.html", context)


@login_required
def delete_post(request, pk):
    if not request.user.has_perm('blogs.delete_blog'):
        messages.warning(request, "You are not eligible to delete this post.")
        return redirect('posts')

    post = get_object_or_404(Blog, pk=pk)
    post.delete()

    messages.success(request, "Post deleted successfully."),
    
    return redirect('posts')

@login_required
def users(request):
    users = User.objects.all()
    context = {
        "users": users,
    }
    return render(request, "dashboard/users.html", context)


@login_required
def add_user(request):
    if not request.user.has_perm('auth.add_user'):
        messages.warning(request, "You are not eligible to add a user.")
        return redirect('users')

    if request.method == "POST":
        form = AddUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "User added successfully.")
            return redirect('users')
    else:
        form = AddUserForm()

    context = {
        "form": form,
    }
    return render(request, "dashboard/add_user.html", context)

def edit_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = EditUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users')
    form = EditUserForm(instance=user)
    context = {
        "form": form,
    }
    return render(request, "dashboard/edit_user.html", context)

def delete_user(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()
    return redirect('users')