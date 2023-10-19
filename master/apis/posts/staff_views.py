from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, UpdateAPIView
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
    

class VerifyBookPostsAPI(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer
    lookup_field = "id"

    # def get_objects(self):
    #     queryset = self.get_queryset()
    #     filtered_queryset = 
    #     data = self.request.data["data"]
    #     for post in data:


    def post(self, request):
        try:
            up_posts = request.data["data"]
            posts = []
            for up_post in up_posts:
                print(up_post["id"])
                post = Post.objects.get(id=up_post["id"])
                if post.is_verified != up_post["is_verified"]:
                    post.is_verified = up_post["is_verified"]
                    post.save()

                posts.append(post)
            # instance = self.get_object()
            # print(instance)
            # serializer = PostsSerializer(instance=instance, data=up_posts, many=True, partial=True)
            # serializer.update()

            return Response({"msg":"success"})
        
        except KeyError as e:
            return Response({"code": "missing_data", "msg": f"missing .{e}" }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        except Exception as e:
            return Response({"code":"post_not_found", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
