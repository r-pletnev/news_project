from django.template.context_processors import request
from news.models import Category


def menu(request):
    category_list = Category.objects.filter(is_hidden=False)
    return {'category_list': category_list}

