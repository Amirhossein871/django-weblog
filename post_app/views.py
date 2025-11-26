from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from .forms import CommentForm
from .models import Post, Category, PostLike, SavedPost
from .filters import PostFilter
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


# Create your views here.

def index(request):
    post_list = Post.objects.filter(status__iexact=Post.StatusChoices.PUBLISHED).order_by('-published_at')
    post_filter = PostFilter(request.GET, queryset=post_list)
    filtered_posts = post_filter.qs

    categories = Category.objects.all()
    paginator = Paginator(filtered_posts, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "post_app/index.html", {
        'page_obj': page_obj,
        'categories': categories,
    })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)

    post.views += 1
    post.save(update_fields=['views'])

    user_like = False
    if request.user.is_authenticated:
        user_like = post.is_user_liked(request.user)

    user_has_saved = False
    if request.user.is_authenticated:
        user_has_saved = SavedPost.objects.filter(user=request.user, post=post).exists()

    if request.method == "POST":
        comment_form = CommentForm(request.POST, user=request.user)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            if request.user.is_authenticated:
                comment.user = request.user
            comment.save()
            messages.success(request, "دیدگاه شما با موفقیت ثبت شد")
            return redirect(post.get_absolute_url())
        else:
            print("error")
    else:
        comment_form = CommentForm(user=request.user)

    context = {
        "post": post,
        "user_like": user_like,
        'user_has_saved': user_has_saved,
        "comment_form": comment_form,
    }
    return render(request, "post_app/post_detail.html", context)


@login_required
def toggle_like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    user = request.user

    like_obj, created = PostLike.objects.get_or_create(user=user, post=post)

    if not created:
        like_obj.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        "liked": liked,
        "likes_count": post.likes.count()
    })


@login_required
def toggle_save(request, slug):
    post = get_object_or_404(Post, slug=slug)
    user = request.user

    saved_obj = SavedPost.objects.filter(post=post, user=user).first()

    if saved_obj:
        saved_obj.delete()
        saved = False
    else:
        SavedPost.objects.create(post=post, user=user)
        saved = True

    return JsonResponse({
        "saved": saved,
    })
