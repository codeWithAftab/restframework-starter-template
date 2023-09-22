from django.urls import path
from master.apis.general import views

urlpatterns = [
    path("prayertime/", views.PrayerTimeAPI.as_view(), name="prayertime"),
    path("quran-sunnah/search/", views.SearchQuranAndSunnahAPI.as_view(), name="quran-sunnah-search"),
] 