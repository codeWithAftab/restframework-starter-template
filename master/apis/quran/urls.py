from django.contrib import admin
from django.urls import path, include
from ..quran import views

urlpatterns = [
    path('chapters/', views.QuranChaptersApi.as_view(), name="quranChapters"),
    path('chapter/<int:chapter_id>/', views.QuranChaptersApi.as_view(), name="quranChapter"),
    path('languages/', views.LanguagesListApi.as_view(), name="language_api"),
    path('chapters/search/', views.SearchQuran.as_view(), name="quranChapters"),
    path('chapter/<int:chapter_id>/search/', views.SearchQuran.as_view(), name="quranChapter"),
]
