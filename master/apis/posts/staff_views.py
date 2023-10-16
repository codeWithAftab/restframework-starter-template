from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .serializers import PostsSerializer, ReplySerializer, CommentSerializer, TagSerializer, CategorySerializer, PostViewSerializer, IslamicBookSerializer
from master.models import Category, Reply, Comment, Tag, Post, PostView, IslamicBook
from master.apis.general.pagination import CustomLimitPagination
from firebase_auth.authentication import FirebaseAuthentication
from django.db.models import Q
from django.utils import timezone
import random
from datetime import timedelta


class GetIslamicPosts(ListAPIView):
    serializer_class = PostsSerializer
    # authentication_classes = [FirebaseStaffAuthentication] will add

    def get_queryset(self):
        book_id = self.request.GET["book_id"]
        return Post.objects.prefetch_related("views").filter(book__book_id=book_id)