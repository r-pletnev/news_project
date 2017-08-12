from django.shortcuts import render, get_object_or_404
from django.views.generic import TemplateView, ListView, DetailView

from rest_framework import viewsets

from .models import Article, Category
from banners.models import banners_to_view
from utils.utils import get_client_ip

from .serializers import ArticleSerializer, CategorySerializer
from .permissions import IsSuperUserOrReadOnly


class IndexView(ListView):
    model = Article
    paginate_by = 12
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        banners_to_view('main', context, self.request)
        return context

    def get_queryset(self):
        return Article.objects.all()

class NewsDetailView(DetailView):
    model = Article

    def get_context_data(self, **kwargs):
        context = super(NewsDetailView, self).get_context_data(**kwargs)
        context['related_articles'] = Article.objects.filter(
            category=self.object.category
        ).exclude(
            id__exact=self.object.pk
        )[:10]

        self.object.update_view_counter()
        return context



class CategoryDetailView(ListView):
    model = Article
    paginate_by = 12
    context_object_name = 'news'
    template_name = 'news/article_category_detail.html'

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Article.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

class HiddenArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.filter(category__is_hidden=True)
    serializer_class = ArticleSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

def PageNotFound(request):
    return render(request, '404.html')
