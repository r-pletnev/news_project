from django.conf import settings
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from news.models import Site

import zipfile


# Create your models here.

class Spider(models.Model):
    name = models.CharField('Имя паука', max_length=50, help_text="ВНИМАНИЕ! ИСПОЛЬЗОВАТЬ ТОЛЬКО ЛАТИНСКИЕ БУКВЫ", unique=True)
    description = models.TextField('Описание', blank=True)
    archive = models.FileField('Zip-архив с пауком', upload_to='spiders/', validators=[FileExtensionValidator(allowed_extensions=['zip'])])
    interval = models.IntegerField('Интервал перед запусками', help_text='В минутах', validators=[MinValueValidator(1)])
    is_active = models.BooleanField('Рабочий', default=False)
    create_at = models.DateTimeField('Создано', default=timezone.now)
    last_run = models.DateTimeField('Последний запуск', blank=True, null=True)
    is_unpacked = models.BooleanField('Распакован', default=False)
    path = models.CharField('Путь к папке с пауком', max_length=500, blank=True, help_text='Если не распакован то пустой')
    target_site = models.ForeignKey(Site)

    def __str__(self):
        return self.name

    def _unzip(self):
        import os
        try:
            archive_dir = os.path.join(settings.MEDIA_ROOT, 'spiders', 'charged', self.name)
            os.makedirs(archive_dir, exist_ok=True)
            zip_file = zipfile.ZipFile(self.archive.path)
            zip_file.extractall(archive_dir)
            zip_file.close()
            self.is_unpacked = True
        except:
            archive_dir = ''
        return archive_dir


    def save(self, *args, **kwargs):
        if self.is_unpacked:
            return super(Spider, self).save(*args, **kwargs)
        self.path = self._unzip()
        super(Spider, self).save(*args, **kwargs)


    class Meta:
        db_table = 'spiders'
        verbose_name = 'Паук'
        verbose_name_plural = 'Пауки'


