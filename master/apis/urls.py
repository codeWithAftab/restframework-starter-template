from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include("master.apis.general.urls")),
    path('quran/', include("master.apis.quran.urls")),
    path('sunnah/', include("master.apis.sunnah.urls")),
]
