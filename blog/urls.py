from django.urls import path
from .views import PostList, PostDetail, VoteCreate, CommentCreate, CommentDetail


app_name = 'blog'

urlpatterns = [
    path('posts/', PostList.as_view(), name='post-list'),
    path('posts/<int:pk>', PostDetail.as_view(), name='post-detail'),
    path('posts/<int:pk>/vote', VoteCreate.as_view(), name='votes'),
    path('posts/<int:pk>/comments', CommentCreate.as_view(), name='comments-list'),
    path('posts/<int:pk>/comments/<int:com>',
         CommentDetail.as_view(), name='comments-detail'),
]
