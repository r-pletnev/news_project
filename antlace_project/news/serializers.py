from rest_framework import serializers
from .models import Article, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('slug', 'name', 'id', 'is_hidden')


class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'description', 'keywords', 'body', 'source_url', 'created_at', 'image_url', 'category')

class HiddenArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ('title', 'description', 'keywords', 'body', 'source_url', 'created_at', 'image_url', 'category')
