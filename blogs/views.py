from django.shortcuts import redirect, render, get_object_or_404

from .models import Blog, Category

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