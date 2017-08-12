from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from utils.utils import get_client_ip


class View(models.Model):
    banner = models.ForeignKey('banners.Banner', verbose_name='Баннер', related_name='views')
    created_at = models.DateTimeField('Дата создания', auto_now_add=True)
    ip = models.GenericIPAddressField(blank=True, null=True)
    meta = models.TextField(blank=True)


    class Meta:
        ordering = ['-created_at']
        db_table = 'views'
        verbose_name = 'Просмотр'
        verbose_name_plural = 'Просмотры'


LAYOUT_CHOICES = (
    (1, 'горизонтально'),
    (2, 'вертикально')
)

PAGE_TYPES = (
    (1, 'main'),
    (2, 'detail')
)

class PageType(models.Model):
    name = models.CharField('Имя', max_length=30)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'page_types'
        verbose_name = 'Тип страницы'
        verbose_name_plural = 'Типы страниц'


class PagePosition(models.Model):
    layout = models.IntegerField('Компоновка', choices=LAYOUT_CHOICES)
    index = models.IntegerField('Индекс', default=1, validators=[MinValueValidator(1), MaxValueValidator(4)], blank=True)
    type = models.IntegerField('Тип страницы', choices=PAGE_TYPES)

    def __str__(self):
        layout = 'Горизонтальная' if self.layout == 1 else 'Вертикальная'
        type = 'Главная' if self.type == 1 else 'Детали'

        return 'Страница "{}" позиция {} на {}'.format(type, layout, self.index)

    class Meta:
        db_table = 'positions'
        verbose_name = 'Позиция'
        verbose_name_plural = 'Позиции на страницах'
        unique_together = (('layout', 'index', 'type'))


class BannerManager(models.Manager):
    def main_page_banners(self):
        return self.filter(is_active=True, position__type=1)

    def detail_page_banners(self):
        return self.filter(is_active=True, position__type=2)

    def active_banners(self):
        return self.filter(is_active=True)

class Banner(models.Model):
    name = models.CharField('Имя', max_length=50, unique=True)
    is_active = models.BooleanField('Активный', default=True)
    code = models.TextField('Код')
    layout = models.IntegerField('Тип', choices=LAYOUT_CHOICES)
    position = models.ForeignKey(PagePosition, verbose_name='Позиция на странице')

    objects = BannerManager()

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'banners'
        verbose_name = 'Баннеры'
        verbose_name_plural = 'Баннеры'


def banners_to_view(page_type, context, request):
    if page_type == 'main':
        banners = list(Banner.objects.main_page_banners())
    else:
        banners = list(Banner.objects.detail_page_banners())

    for banner in banners:
        view = View.objects.create(
            banner=banner,
            ip=get_client_ip(request),
            meta=self.request.META
        )
        view.save()

    banner_dict = {'banner{}'.format(elm.position.index): elm.code for elm in banners}
    context.update(banner_dict)
