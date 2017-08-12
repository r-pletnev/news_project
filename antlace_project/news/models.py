import datetime
from unidecode import unidecode
import urllib.request
import uuid
from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils.text import slugify
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from .utils import get_url_params


class Category(models.Model):
    name = models.CharField('Имя',max_length=50, unique=True)
    description = models.CharField("Описание", blank=True, help_text='Метатег description', max_length=300)
    keywords = models.CharField(blank=True, help_text='Метатег keywords', max_length=300)
    is_hidden = models.BooleanField('Скрытая', help_text='Если скрытая то неотображается в меню сайта', default=False)
    slug = models.SlugField(
        'ЧПУ',
        db_index=True,
        unique=True,
        help_text='Будет использоваться в роутинге')

    def __str__(self):
        return self.slug

    class Meta:
        db_table = 'categories'
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Site(models.Model):
    url = models.URLField('Hostname', unique=True)

    def __str__(self):
        return self.url

    class Meta:
        db_table = 'sites'
        verbose_name = 'Сайт'
        verbose_name_plural = 'Сайты'


class Article(models.Model):
    title = models.CharField("Наименование", db_index=True, max_length=255)
    slug = models.SlugField("ЧПУ", db_index=True, max_length=255, unique=True, blank=True)
    description = models.CharField("Описание", blank=True, help_text='Метатег description', max_length=300)
    keywords = models.CharField(blank=True, help_text='Метатег keywords', max_length=300)
    body = models.TextField('Текст')
    source_url = models.URLField("Источник статьи", unique=True)
    created_at = models.DateTimeField("Дата создания", blank=True, help_text='Если не указано то ставим текущую дату')
    cover_image = models.ImageField("Картинка", upload_to='covers_images', blank=True)
    image_url = models.URLField('Url картинки', blank=True, help_text='Если указать то при сохранении будет закачан файл', max_length=500)
    category = models.ForeignKey('news.Category', verbose_name='Категория', to_field='slug')
    site = models.ForeignKey('news.Site', to_field='url', blank=True, null=True)
    view_counter = models.PositiveIntegerField('число просмотров', default=0)

    def __str__(self):
        return self.title

    def _get_unique_slug(self):
        slug = slugify(unidecode(self.title))
        unique_slug = slug
        num = 1
        while Article.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug, num)
            num += 1
        return unique_slug

    def _upload_image(self):
        img_temp = NamedTemporaryFile()
        img_temp.write(urllib.request.urlopen(self.image_url).read())
        img_temp.flush()
        self.cover_image.save('{}.jpeg'.format(uuid.uuid4()), File(img_temp), save=False)

    def _set_site(self):
        site_url = get_url_params(self.source_url).get('netloc')
        site, _ = Site.objects.get_or_create(url=site_url)
        self.site = site

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self._get_unique_slug()

        if self.image_url and not self.cover_image:
            self._upload_image()

        if not self.created_at:
            self.created_at = datetime.datetime.now()

        self._set_site()

        super(Article, self).save(*args, **kwargs)

    def update_view_counter(self):
        self.view_counter += 1
        self.save()

    def get_absolute_url(self):
        return reverse('news:news_detail', kwargs={'category': self.category, 'slug': self.slug})

    class Meta:
        ordering = ['-created_at']
        db_table = 'news'
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'


