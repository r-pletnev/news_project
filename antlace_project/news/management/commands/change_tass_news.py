from django.core.management.base import BaseCommand, CommandError
from news.models import Article, Category
from urllib.parse import urlparse

def gc(txt):
    return Category.objects.get(slug=txt)

CATS = {
    'forum-v-davose': gc('economics'),
    'kosmos': gc('kosmos'),
    'info': gc('world'),
    'besporyadki-v-egipte': gc('world'),
    'glavnie-novosti': gc('incidents'),
    'proisshestviya': gc('incidents'),
    'delo-eks-mera-yaroslavlya-evgeniya-urlashova': gc('politics'),
    'sochi2014': gc('sport'),
    'kultura': gc('culture'),
    'siriya-konflikt': gc('world'),
    'ekonomika': gc('economics'),
    'armiya-i-opk': gc('army'),
    'delo-edvard-snowden': gc('incidents'),
    'obschestvo': gc('society'),
    'vybory-prezidenta-usa': gc('mezhdunarodnaya-panorama'),
    'situaciya-na-koreyskom-poluostrove': gc('mezhdunarodnaya-panorama'),
    'vybory-na-ukraine': gc('mezhdunarodnaya-panorama'),
    'venecianskiy-kinofestival': gc('culture'),
    'sport': gc('sport'),
    'tass-dos-e-kul-tura': gc('culture'),
    'politika': gc('politics'),
    'arhiv': gc('incidents'),
    'v-centre-vnimaniya': gc('incidents'),
    'raketnye-zapuski-v-kndr': gc('mezhdunarodnaya-panorama'),
    'blizhnee-zarubezhe': gc('mezhdunarodnaya-panorama'),
    'reforma-akademii-nauk': gc('science'),
    'mezhdunarodnaya-panorama': gc('mezhdunarodnaya-panorama'),
    'nauka': gc('science'),
    'migracionnaya-situaciya-v-rf': gc('society'),
    'moskva' : gc('society'),
    'korrupcionnye-skandaly': gc('incidents'),
    'spb-news': gc('society'),
    'reforma-akademii-nauk': gc('science'),
    'mezhdunarodnaya-panorama': gc('mezhdunarodnaya-panorama'),
    'nauka': gc('science'),
}

class Command(BaseCommand):
    help = 'Change task category by it`s source_url'

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
        for article in articles:
            cat_txt = self.get_category(article.source_url)
            if cat_txt == '':
                continue
            category = CATS.get(cat_txt)
            if category is None:
                continue
            article.category = category
            article.save()
                
        
