from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.utils import timezone
from mptt.models import MPTTModel, TreeForeignKey
from utils.text import slugify_unidecode
from django.contrib.auth import get_user_model
from django.shortcuts import reverse

User = get_user_model()


# Create your models here.

class Category(MPTTModel):
    class MPTTMeta:
        order_insertion_by = ['name']

    name = models.CharField(max_length=100, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' / '.join(full_path[::-1])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_unidecode(self.name)
        super().save(*args, **kwargs)


class Post(models.Model):
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    class StatusChoices(models.TextChoices):
        DRAFT = "پیش نویس"
        PUBLISHED = "منتشر شده"

    title = models.CharField(max_length=255, verbose_name="Post Title")
    image = models.ImageField(upload_to="post_img", verbose_name="Post Image")
    excerpt = models.TextField(blank=True, null=True, verbose_name="Post Summary")
    content = RichTextUploadingField(verbose_name="Post Body")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Post Author", related_name='author')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Post Created")
    category = TreeForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts',
        verbose_name="Post Category"
    )
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Post Updated")
    slug = models.SlugField(max_length=255, verbose_name="Post Slug", unique=True)
    status = models.CharField(max_length=20, choices=StatusChoices.choices, verbose_name="Post Status",
                              default=StatusChoices.DRAFT)
    views = models.PositiveIntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Post Published")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify_unidecode(self.title)

        if self.status == self.StatusChoices.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()

        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail', kwargs={'slug': self.slug})

    def likes_count(self):
        return self.likes.count()


class PostLike(models.Model):
    class Meta:
        verbose_name = "Post Like"
        verbose_name_plural = "Post Likes"
        unique_together = ('user', 'post')

    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Post Like", related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Post Like")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Post Created")

    def __str__(self):
        return f'post:{self.post.get_absolute_url()};user:{self.user.email}'


class SavedPost(models.Model):
    class Meta:
        verbose_name = "Saved Post"
        verbose_name_plural = "Saved Posts"
        unique_together = ('user', 'post')

    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Saved Post")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Saved Post", related_name='saved_posts')
    saved_at = models.DateTimeField(auto_now_add=True, verbose_name="Saved Created")


class Comment(models.Model):
    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"

    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Comment", related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Comment")
    comment = models.TextField(verbose_name="Comment")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Comment Created")

    def __str__(self):
        return f'post:{self.post.get_absolute_url()};user:{self.user.email};comment:{self.comment}'
