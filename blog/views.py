from weakref import ProxyTypes
from rest_framework import generics, permissions, mixins, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from .models import Post, Vote, Comment
from .serializers import PostSerializer, VoteSerializer, CommentSerializer
from .permissions import PostUserWritePermission

# Create your views here.


class PostList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Post.postobjects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [PostUserWritePermission]
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class VoteCreate(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = VoteSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Vote.objects.filter(voter=user, post=post)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('You have already voted for this post :)')
        serializer.save(voter=self.request.user,
                        post=Post.objects.get(pk=self.kwargs['pk']))

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('You have not voted for this post!')


class CommentCreate(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        post=Post.objects.get(pk=self.kwargs['pk']))


class CommentDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [PostUserWritePermission]
    lookup_url_kwarg = 'com'

    def get_queryset(self):
        post = Post.objects.get(pk=self.kwargs['pk'])
        return Comment.objects.filter(post=post)
