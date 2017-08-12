# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Spider


@admin.register(Spider)
class SpiderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'archive',
        'interval',
        'is_active',
        'create_at',
        'last_run',
        'is_unpacked',
        'path',
        'target_site',
    )
    list_filter = (
        'is_active',
        'create_at',
        'last_run',
        'is_unpacked',
        'target_site',
    )
    search_fields = ('name',)
