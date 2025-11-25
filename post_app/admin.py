from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Post, PostLike, SavedPost, Comment


# Register your models here.

@admin.register(Category)
class CategoryAdmin(MPTTModelAdmin):
    list_display = ('name', 'slug', 'parent')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('tree_id', 'lft')
    list_filter = ('parent',)
    mptt_level_indent = 20


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'author', 'category', 'status',
        'views', 'likes_count', 'created_at', 'published_at'
    )
    list_filter = ('status', 'category', 'author', 'published_at')
    search_fields = ('title', 'excerpt', 'content')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'updated_at', 'published_at')
    date_hierarchy = 'created_at'

    fieldsets = (
        ('General Info', {
            'fields': ('title', 'slug', 'author', 'status', 'category', 'image')
        }),
        ('Summary & Content', {
            'fields': ('excerpt', 'content')
        }),
        ('Statistics', {
            'fields': ('views',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'published_at')
        }),
    )

    def likes_count(self, obj):
        return obj.likes.count()

    likes_count.short_description = 'Likes'


@admin.register(PostLike)
class PostLikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at')
    list_filter = ('created_at', 'post')
    search_fields = ('post__title', 'user__email')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)


@admin.register(SavedPost)
class SavedPostAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'saved_at')
    list_filter = ('saved_at', 'post')
    search_fields = ('post__title', 'user__email')
    readonly_fields = ('saved_at',)
    ordering = ('-saved_at',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'guest_name', 'guest_email', 'short_comment', 'created_at')
    list_filter = ('post', 'created_at')
    search_fields = ('user__email', 'comment', 'post__title', 'guest_name', 'guest_email')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def short_comment(self, obj):
        return (obj.comment[:50] + '...') if len(obj.comment) > 50 else obj.comment

    short_comment.short_description = 'Comment Preview'
