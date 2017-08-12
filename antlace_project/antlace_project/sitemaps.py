from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from news.models import Article

class ArticleSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.5
    limit = 50000

    def items(self):
        return Article.objects.all()




