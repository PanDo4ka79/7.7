from django.shortcuts import render, get_object_or_404
from .models import Post
from django.core.paginator import Paginator
from django_filters import rest_framework as filters
from django.forms import DateInput
from .filters import PostFilter
from django.urls import  reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView
from .forms import PostForm



def news_list(request):
    news = Post.objects.filter(category_type=Post.NEWS).order_by('-created_at')
    return render(request, 'news/news_list.html', {'news': news})


def news_detail(request, pk):
    news = get_object_or_404(Post, pk=pk, category_type=Post.NEWS)
    return render(request, 'news/news_detail.html', {'news': news})


def news_list2(request):
    news = Post.objects.all().order_by('-created_at')
    paginator = Paginator(news, 10)  # 10 новостей на страницу

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'news/news_list.html', {'page_obj': page_obj})


class PostFilter(filters.FilterSet):
    title = filters.CharFilter(lookup_expr='icontains')
    author__user__username = filters.CharFilter(lookup_expr='icontains', label='Автор')
    created_at = filters.DateFilter(widget=DateInput(attrs={'type': 'date'}), lookup_expr='gte', label='Позже даты')

    class Meta:
        model = Post
        fields = ['title', 'author__user__username', 'created_at']


def news_search(request):
    post_filter = PostFilter(request.GET, queryset=Post.objects.all())
    return render(request, 'news/news_search.html', {'filter': post_filter})

class PostCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'
    success_url = reverse_lazy('news_list')

class PostUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'
    success_url = reverse_lazy('news_list')

class PostDeleteView(DeleteView):
    model = Post
    template_name = 'news/post_confirm_delete.html'
    success_url = reverse_lazy('news_list')