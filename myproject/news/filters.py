import django_filters
from django.forms import DateInput
from .models import Post  # Импортируйте модель Post

class PostFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='icontains', label='Title')
    author = django_filters.CharFilter(field_name='author__user__username', lookup_expr='icontains', label='Author')
    date_published = django_filters.DateFilter(
        field_name='date_published',
        lookup_expr='gte',
        widget=DateInput(attrs={'type': 'date'}),
        label='Published after'
    )

    class Meta:
        model = Post
        fields = ['title', 'author', 'date_published']
