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


class GetIslamicPostsAPI(ListAPIView):
    serializer_class = PostsSerializer
    # authentication_classes = [FirebaseStaffAuthentication] will add

    def get_queryset(self):
        book_id = self.request.GET["book_id"]
        filter = self.request.GET.get('filter')
        if filter == "verified":
            return Post.objects.prefetch_related("views").filter(book__book_id=book_id, is_verified=True)
        
        elif filter == "un-verified":
            return Post.objects.prefetch_related("views").filter(book__book_id=book_id, is_verified=False)
        
        return Post.objects.prefetch_related("views").filter(book__book_id=book_id)
    

class VerifyBookPostsAPI(APIView):
    def post(self, request):
        try:
            post_id = request.data["post_id"]
            post = Post.objects.get(id=post_id)
            post.is_verified = True
            post.save()
            return Response({"msg":"success", "data": PostsSerializer(post, context={"request":request}).data, })
        
        except KeyError as e:
            return Response({"code": "missing_post_id", "msg": f"post_id is mandatory.{e}" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            return Response({"code":"post_not_found", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
