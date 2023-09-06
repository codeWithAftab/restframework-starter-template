from django.urls import path
from master.apis.general import views

urlpatterns = [
    path("categories/", views.GetCategoryListApi.as_view(), name="categories"),
    path("tags/", views.GetTagsListApi.as_view(), name="tags"),
    path("posts/", views.GetPostsApi.as_view(), name="posts"),
    path("post/<int:post_id>/like/", views.LikeUnlikePostApi.as_view(), name="like"),
    path("post/<int:post_id>/comment/", views.CommentApi.as_view(), name="comment"),
    path("post/comment/<int:comment_id>/reply/", views.ReplyCommentApi.as_view(), name="replies"),
] 