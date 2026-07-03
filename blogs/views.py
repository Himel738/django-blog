
from django.shortcuts import redirect, render, get_object_or_404
from .models import Blog, Category
from django.db.models import Q

# Create your views here.
def post_by_category(request, category_id):
    posts = Blog.objects.filter(category_id=category_id, status='Published').order_by('updated_at')
    # try:
    #     category = Category.objects.get(pk=category_id)
    # except:
    #     return redirect('home')  # Redirect to home if category does not exist

    category = get_object_or_404(Category, pk=category_id)


    context = {
        "posts": posts,
        "category": category,
    }
    return render(request, 'post_by_category.html', context)

def blogs(request, slug):
    single_blog = get_object_or_404(Blog, slug=slug, status='Published')
    context ={
        'single_blog': single_blog
    }
    return render (request, 'blogs.html', context)

def search(request):
    keyword = request.GET.get('keyword')
    blogs = Blog.objects.filter(Q(title__icontains=keyword) | Q(short_description__icontains=keyword) | Q(blog_body__icontains=keyword), status='Published').order_by('updated_at')

    context = {
        "blogs": blogs,
        "keyword": keyword
    }
    return render(request, 'search.html', context)