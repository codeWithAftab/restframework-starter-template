from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .serializers import PostsSerializer, ReplySerializer, CommentSerializer, TagSerializer, CategorySerializer, PostViewSerializer
from master.models import Category, Reply, Comment, Tag, Post, PostView
from master.apis.general.pagination import CustomLimitPagination
from firebase_auth.authentication import FirebaseAuthentication
from .recomendation import PostRecomender
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta

class CustomListAPIView(ListAPIView):
    def __init__(self) -> None:
        self.is_many = True

    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=self.is_many)
        response = {
            "data": serializer.data
        }
        return Response(response)

class ExtendedAPIViewclass(APIView):
    def _handle_missing_post_id(self):
        return Response({"error_code": "missing_post_id", "msg": "Missing post_id in URL."}, status=status.HTTP_400_BAD_REQUEST)

    def _handle_post_not_found(self):
        return Response({"error_code": "post_not_found", "msg": "Post not found."}, status=status.HTTP_404_NOT_FOUND)

    def _handle_already_liked(self):
        return Response({"error_code": "already_liked", "msg": "Already Liked"}, status=status.HTTP_400_BAD_REQUEST)

    def _handle_already_disliked(self):
        return Response({"error_code": "already_disliked", "msg": "Already Disliked"}, status=status.HTTP_400_BAD_REQUEST)

    def _handle_comment_not_found(self):
        return Response({"error_code": "comment_not_found", "msg": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
    
    def _handle_already_removed(self):
        return Response({"error_code": "comment_removed_already", "msg": "Already removed comment"}, status=status.HTTP_400_BAD_REQUEST)
    
    def _handle_reply_not_found(self):
        return Response({"error_code": "reply_not_found", "msg": "Reply not found."}, status=status.HTTP_404_NOT_FOUND)
    
class GetTagsListAPI(CustomListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class GetCategoryListAPI(CustomListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class GetPostsAPI(ListAPIView):
    serializer_class = PostsSerializer
    pagination_class = CustomLimitPagination
    authentication_classes = [FirebaseAuthentication]

    def get_queryset(self):
        user = self.request.user
        # Calculate the date 1 month ago from the current date
        one_month_ago = timezone.now() - timedelta(days=30)
        queryset = Post.objects.exclude(Q(views__user=user) & Q(views__last_view__gt=one_month_ago))

        recomender = PostRecomender(user=user, posts=queryset, top_n=100)
        return recomender.get_prefered_posts()

class LikeUnlikePostAPI(ExtendedAPIViewclass):
    authentication_classes = [FirebaseAuthentication]

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
        
class CommentAPI(ExtendedAPIViewclass):
    authentication_classes = [FirebaseAuthentication]

    def get(self, request, post_id=None):
        if not post_id:
           return self._handle_missing_post_id()
        
        try:
            post = Post.objects.get(id=post_id)
            comments = post.get_comments()
            response = {
                "data": CommentSerializer(comments, many=True).data
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
            comment_msg = request.data["comment_msg"]

            post = Post.objects.get(id=post_id)
            
            comment = post.do_comment(user=request.user, content=comment_msg)

            response = {
                "data": CommentSerializer(comment).data
            }
            return Response(response, status=status.HTTP_201_CREATED)

        except Post.DoesNotExist:
            return self._handle_post_not_found()
        except Exception as e:
            return Response({"error_code": "internal_server_error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, post_id=None):
        if not post_id:
            return self._handle_missing_post_id()

        try:
            comment_id = request.data["comment_id"]
            post = Post.objects.get(id=post_id)

            try:
                post.remove_comment(user=request.user, comment_id=comment_id)

            except Comment.DoesNotExist:
                return self._handle_comment_not_found()
            
            return Response({"msg":"Comment Removed"}, status=status.HTTP_204_NO_CONTENT)

        except Post.DoesNotExist:
            return self._handle_post_not_found()

        except Exception as e:
            return Response({"error_code": "internal_server_error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
        
class ReplyCommentAPI(ExtendedAPIViewclass):
    authentication_classes = [FirebaseAuthentication]

    def get(self, request, comment_id=None):
        if not comment_id:
           return self._handle_missing_post_id()
        
        try:
            comment = Comment.objects.get(id=comment_id, is_removed=False)
            replies = comment.get_replies()
            response = {
                "data": ReplySerializer(replies, many=True).data
            }
            return Response(response)

        except Comment.DoesNotExist:
            return self._handle_comment_not_found()
        except Exception as e:
            return Response({"error_code": "internal_server_error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def post(self, request, comment_id=None):
        if not comment_id:
           return self._handle_missing_post_id()

        try:
            reply_msg = request.data["reply_msg"]

            comment = Comment.objects.get(id=comment_id)
            
            reply = comment.do_reply(user=request.user, content=reply_msg)
            
            response = {
                "data": ReplySerializer(reply).data
            }
            return Response(response, status=status.HTTP_201_CREATED)

        except Comment.DoesNotExist:
            return self._handle_comment_not_found()
        
        except Exception as e:
            return Response({"error_code": "internal_server_error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, comment_id=None):
        if not comment_id:
            return self._handle_missing_comment_id()

        try:
            reply_id = request.data["reply_id"]
            comment = Comment.objects.get(id=comment_id)

            try:
                comment.remove_reply(user=request.user, reply_id=reply_id)

            except Reply.DoesNotExist:
                return self._handle_reply_not_found()
            
            return Response({"msg":"Reply Removed"}, status=status.HTTP_204_NO_CONTENT)

        except Comment.DoesNotExist:
            return self._handle_comment_not_found()

        except Exception as e:
            return Response({"error_code": "internal_server_error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   
        
class LikeUnlikeCommentAPI(ExtendedAPIViewclass):
    authentication_classes = [FirebaseAuthentication]

    def get(self, request, post_id=None, comment_id=None):
        if not post_id:
           return self._handle_missing_post_id()
        
        try:
            comment = Comment.objects.get(user=request.user, id=comment_id)
            context = {
                "show_liked_users":True
            }
            response = {
                "data": CommentSerializer(comment, context=context).data
            }
            return Response(response)

        except Post.DoesNotExist:
            return self._handle_post_not_found()
        except Exception as e:
            return Response({"error_code": "internal_server_error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


    def post(self, request, post_id=None, comment_id=None):
        if not post_id:
           return self._handle_missing_post_id()

        try:
            comment = Comment.objects.get(post__id=post_id, id=comment_id)
            if comment.liked(user=request.user):
                return self._handle_already_liked()
            
            comment.increase_like(user=request.user)
            response = {
                "data": CommentSerializer(comment).data
            }
            return Response(response)

        except Post.DoesNotExist:
            return self._handle_post_not_found()
        except Exception as e:
            return Response({"error_code": "internal_server_error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def delete(self, request, post_id=None, comment_id=None):
        if not post_id:
            return self._handle_missing_post_id()

        try:
            comment = Comment.objects.get(post__id=post_id, id=comment_id)
            if not comment.liked(user=request.user):
                return self._handle_already_disliked()
            
            comment.decrease_like(user=request.user)  
            response = {
                "data": CommentSerializer(comment).data
            }
            return Response(response)

        except Post.DoesNotExist:
            return self._handle_post_not_found()

        except Exception as e:
            return Response({"error_code": "internal_server_error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)   

class PostViewsAPI(ExtendedAPIViewclass):
    authentication_classes = [FirebaseAuthentication]

    def get(self, request, post_id=None):
        if not post_id:
           return self._handle_missing_post_id()
        
        try:
            post_views = PostView.objects.filter(user=request.user)
            response = {
                "data": PostViewSerializer(post_views, many=True).data
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
        except Post.DoesNotExist:
            return self._handle_post_not_found()
        
        try:
            post_view = PostView.objects.get(user=request.user, post=post)
            post_view.count += 1
            post_view.save()

        except PostView.DoesNotExist:
            post_view = PostView.objects.create(user=request.user, post=post)
        
        try:
            serializer = PostViewSerializer(post_view)
            response = {
                "data": serializer.data
            }
            return Response(response)

        except Exception as e:
            return Response({"error_code": "internal_server_error", "msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        