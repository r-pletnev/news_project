# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import View, PagePosition, Banner


@admin.register(View)
class ViewsAdmin(admin.ModelAdmin):
    list_display = ('id', 'banner', 'created_at', 'ip', 'meta')
    list_filter = ('banner', 'created_at')
    date_hierarchy = 'created_at'


@admin.register(PagePosition)
class PagePositionAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'index')


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active', 'code', 'layout', 'position')
    list_filter = ('is_active', 'position')
    search_fields = ('name',)
