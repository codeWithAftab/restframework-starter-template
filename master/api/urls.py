from django.urls import path
from master.api import views

urlpatterns = [
    path("categories/", views.GetCategoryListApi.as_view(), name="get_categories"),
    path("tags/", views.GetTagsListApi.as_view(), name="get_tags"),
    path("posts/", views.GetPostsApi.as_view(), name="get_systems_posts"),
    path("post/<int:post_id>/like/", views.LikeUnlikePostApi.as_view(), name="like")
] 