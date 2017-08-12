from django.conf.urls import url, include
from rest_framework import routers
from .views import IndexView, NewsDetailView, CategoryDetailView, ArticleViewSet, HiddenArticleViewSet, CategoryViewSet


router = routers.DefaultRouter()
router.register('hidden', HiddenArticleViewSet, 'hidden')
router.register('categories', CategoryViewSet)
router.register('articles', ArticleViewSet)

app_name ='news'

urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'page/(?P<page>\d+)/$', IndexView.as_view(), name='news_paginator'),
    url(r'(?P<slug>[-\w]+)/(?P<page>\d+)/$', CategoryDetailView.as_view(), name='category_paginator'),
    url(r'(?P<category>[-\w]+)/article/(?P<slug>[-\w]+)/$', NewsDetailView.as_view(), name='news_detail'),
    url(r'(?P<slug>[-\w]+)/$', CategoryDetailView.as_view(), name='category_detail'),
    url(r'$', IndexView.as_view(), name='index_page'),
]
