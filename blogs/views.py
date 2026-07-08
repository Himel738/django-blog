
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from .models import Blog, Category
from django.db.models import Q
from .models import Comment

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

    if request.method == 'POST':
       comment = Comment()
       comment.user = request.user
       comment.blog = single_blog
       comment.comment = request.POST['comment']
       comment.save()
       return HttpResponseRedirect(request.path_info)
    # Comments
    comments = Comment.objects.filter(blog=single_blog).order_by('-created_at')
    comment_count = comments.count()
    context ={
        'single_blog': single_blog,
        'comments': comments,
        'comment_count': comment_count
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