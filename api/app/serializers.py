from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.db import models
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ['id', 'title', 'author', 'email']