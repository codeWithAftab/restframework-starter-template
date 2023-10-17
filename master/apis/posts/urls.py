from django.urls import path
from master.apis.posts import views
from master.apis.posts import staff_views

urlpatterns = [
    path("categories/", views.GetCategoryListAPI.as_view(), name="categories"),
    path("tags/", views.GetTagsListAPI.as_view(), name="tags"),
    path("posts/", views.GetPostsAPI.as_view(), name="posts"),
    path("posts/islamic-books/", views.GetBooks.as_view(), name="books"),
    path("posts/user-liked/", views.GetUserLikedPost.as_view(), name="liked-post"),
    path("post/<int:post_id>/like/", views.LikeUnlikePostAPI.as_view(), name="like"),
    path("post/<int:post_id>/view/", views.PostViewsAPI.as_view(), name="view"),
    path("post/<int:post_id>/comment/", views.CommentAPI.as_view(), name="comment"),
    path("post/<int:post_id>/comment/<int:comment_id>/like/", views.LikeUnlikeCommentAPI.as_view(), name="comment_like"),
    path("post/comment/<int:comment_id>/reply/", views.ReplyCommentAPI.as_view(), name="replies")
] 

staff_urlpatterns = [
    path("staff/posts/", staff_views.GetIslamicPostsAPI.as_view(), name="get_posts"),
    path("staff/posts/verify-post/", staff_views.VerifyBookPostsAPI.as_view(), name="verify-post"),
] 

urlpatterns += staff_urlpatterns