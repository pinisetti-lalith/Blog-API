from typing import SupportsRound
from django.db import models
from rest_framework import serializers
from .models import Post, Vote, Comment


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    votes = serializers.SerializerMethodField('get_votes')

    class Meta:
        model = Post
        fields = ('id', 'title', 'author', 'excerpt',
                  'content', 'status', 'image_url', 'votes',)

    def get_votes(self, post):
        return Vote.objects.filter(post=post).count()


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id']


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    author_id = serializers.ReadOnlyField(source='author.id')
    post_id = serializers.ReadOnlyField(source='post.id')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'author_id', 'post_id', 'comment']

    def get_post(self, post):
        return Comment.objects.filter(post=post)
