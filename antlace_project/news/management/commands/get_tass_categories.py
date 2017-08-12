from django.core.management.base import BaseCommand, CommandError
from news.models import Article
from urllib.parse import urlparse

class Command(BaseCommand):
    help = 'Print out list all categories from tass source url'

    def get_category(self, txt):
        try:
            result = urlparse(txt)
            if result.netloc != 'tass.ru':
                return ''
            path = result.path
            return path.split('/')[1]
        except:
            return ''
    
    
    def handle(self, *args, **options):
        articles = Article.objects.all()
        out = set([])
        for article in articles:
            out.add(self.get_category(article.source_url))
        
        self.stdout.write(out, ending='')
