from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from .models import Post, Category


# Create your views here.

def index(request):
    post_list = Post.objects.all().order_by('-published_at')
    categories = Category.objects.all()
    paginator = Paginator(post_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "post_app/index.html", {
        'page_obj': page_obj,
        'categories': categories,
    })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    post.views += 1
    post.save()
    return render(request, "post_app/post_detail.html", {
        'post': post,
    })
