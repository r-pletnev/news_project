# -*- coding: utf-8 -*-
from django.contrib import admin

from .models import Article, Category, Site


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'slug',
        'category',
        'view_counter',
        'source_url',
        'site'
    )
    raw_id_fields = ('category', 'site')
    search_fields = ('slug',)
    list_filter = ('site', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'description',
        'keywords',
        'is_hidden',
        'slug',
    )
    list_filter = ('is_hidden',)
    search_fields = ('name', 'slug')
    prepopulated_fields = {'slug': ['name']}

@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    list_display = ('id', 'url')
