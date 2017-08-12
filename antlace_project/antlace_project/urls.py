"""antlace_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView
from django.views.generic import TemplateView

from django.contrib.sitemaps.views import sitemap, index 
from django.views.decorators.cache import cache_page
from .sitemaps import ArticleSitemap

from rest_framework.authtoken import views


sitemaps = {
    'articles': ArticleSitemap
}



urlpatterns = [
    url(r'^404/$', TemplateView.as_view(template_name='404.html'), name='404'),
    url(r'^robots\.txt/?$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain')),
    url(r'^token/$', views.obtain_auth_token),
    url(r'^admin/', admin.site.urls),
    url(r'^sitemap\.xml/?$', cache_page(86400)(index), {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemaps'}),
    url(r'^sitemap-(?P<section>.+)\.xml$', cache_page(86400)(sitemap), {'sitemaps': sitemaps}, 
    name='sitemaps'),
    url(r'', include('news.urls', namespace='news')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

handler404 = 'news.views.PageNotFound'
