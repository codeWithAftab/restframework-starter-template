from django.contrib import admin
from django.urls import path, include
from ..sunnah import views

urlpatterns = [
    path('collections/', views.SunnahCollectionAPI.as_view(), name="sunnahCollection"),
    path('collection/<int:collection_id>/books/', views.SunnahBookAPI.as_view(), name="sunnahCollectionbOOKS"),
    path('collection/<int:collection_id>/search/', views.SunnahVerseSearchAPI.as_view(), name="sunnahCollectionbOOKS"),

]
