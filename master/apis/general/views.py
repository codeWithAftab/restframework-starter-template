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
        
class CommentApi(APIView):
    authentication_classes = [FirebaseAuthentication]

    def _handle_missing_post_id(self):
        return Response({"error_code": "missing_post_id", "msg": "Missing post_id in URL."}, status=status.HTTP_400_BAD_REQUEST)

    def _handle_post_not_found(self):
        return Response({"error_code": "post_not_found", "msg": "Post not found."}, status=status.HTTP_404_NOT_FOUND)
    
    def _handle_comment_not_found(self):
        return Response({"error_code": "comment_not_found", "msg": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
    
    def _handle_already_removed(self):
        return Response({"error_code": "comment_removed_already", "msg": "Already removed comment"}, status=status.HTTP_400_BAD_REQUEST)
    
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
        
class ReplyCommentApi(APIView):
    authentication_classes = [FirebaseAuthentication]

    def _handle_missing_comment_id(self):
        return Response({"error_code": "missing_comment_id", "msg": "Missing comment_id in URL."}, status=status.HTTP_400_BAD_REQUEST)

    def _handle_comment_not_found(self):
        return Response({"error_code": "comment_not_found", "msg": "Comment not found."}, status=status.HTTP_404_NOT_FOUND)
    
    def _handle_reply_not_found(self):
        return Response({"error_code": "reply_not_found", "msg": "Reply not found."}, status=status.HTTP_404_NOT_FOUND)
    
    def _handle_already_removed(self):
        return Response({"error_code": "reply_removed_already", "msg": "Already removed reply"}, status=status.HTTP_400_BAD_REQUEST)
    
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
        
