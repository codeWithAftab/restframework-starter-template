from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from .serializers import PostsSerializer, ReplySerializer, CommentSerializer, TagSerializer, CategorySerializer
from master.models import Category, Reply, Comment, Tag, Post
from .pagination import CustomLimitPagination
from firebase_auth.authentication import FirebaseAuthentication
import datetime
from .prayertime import PrayTimes
import requests
import json


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
    
    
    
    
class GetTagsListApi(CustomListAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

class GetCategoryListApi(CustomListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

   
class GetPostsApi(ListAPIView):
    queryset = Post.objects.prefetch_related('tags').all()
    serializer_class = PostsSerializer
    pagination_class = CustomLimitPagination

class LikeUnlikePostApi(APIView):
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
        
class CommentApi(ExtendedAPIViewclass):
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
        
class ReplyCommentApi(ExtendedAPIViewclass):
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
        
class LikeUnlikeComment(ExtendedAPIViewclass):
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
        
# class NamazTimingByDate_v3(APIView):
#     """
#     in this api we does'nt depend any other 3rd party api. We have our own prayertime
#     calculation algorithm.
#     """

#     #  latitude, longitude
#     def get(self, request):
#         try:
#             latitude = float(request.query_params["latitude"])
#             longitude = float(request.query_params["longitude"])
#             convention = request.query_params.get("convention","Karachi")
#             date_str = request.query_params.get("date")

#             # if date not provide take current date automatically
#             if not date_str:
#                 curr_date = datetime.date.today()
#             else:
#                 curr_date = datetime.datetime.strptime(
#                     date_str.replace("-", " "), "%d %m %Y")

#             try:
#                 # response = requests.request("GET", url)
#                 # prayTime = PrayTimes()
#                 data = {
#                     "status": 200
#                 }
#                 # Set the coordinates of your location
#                 # Set the date for which you want to calculate prayer times

#                 # Initialize the PrayTimes object with your location and calculation method
#                 pt = prayertimes.PrayTimes(convention)
#                 pt.setMethod(convention)
#                 print("yahan bhi pahuncha")
#                 # Convert the Gregorian date to a Hijri date
#                 hijri_date = convert.Gregorian(curr_date.year, curr_date.month, curr_date.day).to_hijri()
#                 # Calculate prayer times for the given date
#                 data["data"]  = pt.getTimes((curr_date.year, curr_date.month, curr_date.day), (latitude, longitude),hijri=hijri_date)
               
#                 return Response(data, status=status.HTTP_200_OK)

#             except Exception as e:
#                 return Response({"msg": str(e)}, status=status.HTTP_404_NOT_FOUND)

#         except KeyError as e:
#             return Response(f"Missing parameter {[str(e)]}", status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#     def post(self, request):
#         try:
#             latitude = float(request.data["latitude"])
#             longitude = float(request.data["longitude"])
#             convention = request.data.get("convention",'Karachi')
#             date_str = request.data.get("date")
   
#             # if date not provide take current date automatically
#             if not date_str:
#                 curr_date = datetime.date.today()
#             else:
#                 curr_date = datetime.datetime.strptime(
#                     date_str.replace("-", " "), "%d %m %Y")

  
#             try:
#                 # Initialize the PrayTimes object with your location and calculation method
#                 prayer_time = PrayTimes(convention)
#                 prayer_time.setMethod(convention)
#                 # Convert the Gregorian date to a Hijri date
#                 hijri_date = convert.Gregorian(curr_date.year, curr_date.month, curr_date.day).to_hijri()
                
#                 # Calculate prayer times for the given date
#                 times = prayer_time.getTimes(curr_date, (latitude, longitude),hijri=hijri_date)
               
#                 return Response(data, status=status.HTTP_200_OK)
#             except Exception as e:
#                 return Response({"msg":str(e)},status=status.HTTP_404_NOT_FOUND)
#         except KeyError as e:
#             return Response(f"Missing parameter {[str(e)]}", status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"msg": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PrayerTimeAPI(APIView):
    def post(self, request):
        try:
            latitude = request.data["latitude"]
            longitude = request.data["longitude"]
            month = request.data["month"]
            year = request.data["year"]
            print("hello")
            url = f"http://api.aladhan.com/v1/calendar?latitude={latitude}&longitude={longitude}&method=2&month={month}&year={year}"
            print(url)
            try:
                response = requests.request("GET", url)
                data = response.json()
                return Response(data, status=status.HTTP_200_OK)
            except:
                return Response(status=status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            return Response(f"Missing parameter {[str(e)]}", status=status.HTTP_404_NOT_FOUND)
        except:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)