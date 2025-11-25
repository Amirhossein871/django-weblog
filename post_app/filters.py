import django_filters
from .models import Post


class PostFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label='جستجو')
    category = django_filters.CharFilter(field_name='category__name', lookup_expr='icontains', label='دسته',)
    ordering = django_filters.OrderingFilter(
        fields=(
            ('published_at', 'published_at'),
            ('views', 'views'),
        ),
        field_labels={
            'published_at': 'تاریخ انتشار',
            'views': 'تعداد بازدید',
        },
        label='مرتب‌سازی'
    )

    class Meta:
        model = Post
        fields = ['search', 'category']

    def filter_search(self, queryset, name, value):
        return queryset.filter(title__icontains=value)

