from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .serializers import PostsSerializer, ReplySerializer, CommentSerializer, TagSerializer, CategorySerializer
from master.models import Category, Reply, Comment, Tag, Post
from rest_framework.pagination import LimitOffsetPagination
from firebase_auth.authentication import FirebaseAuthentication


class GetTagsListApi(ListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_queryset(), many=True)
            response = {
                "data":serializer.data
            }
            return Response(response)

        except Exception as e:
            return Response({"msg":f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class GetCategoryListApi(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_queryset(), many=True)
            response = {
                "data":serializer.data
            }
            return Response(response)

        except Exception as e:
            return Response({"msg":f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetPostsApi(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostsSerializer

    def get(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(self.get_queryset(), many=True)
            response = {
                "data":serializer.data
            }
            return Response(response)

        except Exception as e:
            return Response({"msg":f"{e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
class LikeUnlikePostApi(APIView):
    authentication_classes = [FirebaseAuthentication]

    def _handle_missing_post_id(self):
        return Response({"error_code": "missing_post_id", "msg": "Missing post_id in URL."}, status=status.HTTP_400_BAD_REQUEST)

    def _handle_post_not_found(self):
        return Response({"error_code": "post_not_found", "msg": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

    def _handle_already_liked(self):
        return Response({"error_code": "already_liked", "msg": "Already Liked"}, status=status.HTTP_400_BAD_REQUEST)

    def _handle_already_disliked(self):
        return Response({"error_code": "already_disliked", "msg": "Already Disliked"}, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, post_id=None):
        if not post_id:
           return self._handle_missing_post_id()
        
        try:
            post = Post.objects.get(id=post_id)
            context = {
                "show_liked_users":True
            }
            response = {
                "data": PostsSerializer(post, context=context).data
            }
            return Response(response)

        except Post.DoesNotExist:
            return self._handle_post_not_found()
        except Exception as e:
            return Response({"error_code": "internal_server_error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


    def post(self, request, post_id=None):
        if not post_id:
           return self._handle_missing_post_id()

        try:
            post = Post.objects.get(id=post_id)
            if post.liked(user=request.user):
                return self._handle_already_liked()
            
            post.increase_like(user=request.user)
            response = {
                "data": PostsSerializer(post).data
            }
            return Response(response)

        except Post.DoesNotExist:
            return self._handle_post_not_found()
        except Exception as e:
            return Response({"error_code": "internal_server_error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, post_id=None):
        if not post_id:
            return self._handle_missing_post_id()

        try:
            post = Post.objects.get(id=post_id)
            if not post.liked(user=request.user):
                return self._handle_already_disliked()
            
            post.decrease_like(user=request.user)  
            response = {
                "data": PostsSerializer(post).data
            }
            return Response(response)

        except Post.DoesNotExist:
            return self._handle_post_not_found()

        except Exception as e:
            return Response({"error_code": "internal_server_error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
        

# class UnlikePostApi(APIView):
#     def post(self,        request, post_id=None):
#         if not post_id:
#             return Response({"error_code": "missing_post_id", "msg": "Missing post_id in URL."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             post = Post.objects.get(id=post_id)
#             if not post.liked(user=request.user):
#                 return Response({"error_code": "already_disliked", "msg": "Already Disliked"}, status=status.HTTP_400_BAD_REQUEST)
            
#             post.decrease_like(user=request.user)  # Assuming you have a decrease_like method
#             response = {
#                 "data": PostsSerializer(post).data
#             }
#             return Response(response)

#         except Post.DoesNotExist:
#             return Response({"error_code": "post_not_found", "msg": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"error_code": "internal_server_error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
# # class GetPostLikedUser(APIView):
    