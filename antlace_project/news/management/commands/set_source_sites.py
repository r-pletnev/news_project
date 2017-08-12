from django.core.management.base import BaseCommand
from news.models import Article, Site
from news.utils import get_url_params


class Command(BaseCommand):
    help = 'Set site by source_url'

    def get_url(self, txt):
        return get_url_params(txt).get('netloc')

    def handle(self, *args, **option):
        ars = Article.objects.all()
        for article in ars:
            site_url = self.get_url(article.source_url)

            if site_url is None:
                continue

            site, _ = Site.objects.get_or_create(url=site_url)
            article.site = site
            article.save()


