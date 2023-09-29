from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from firebase_auth.authentication import FirebaseAuthentication
from master.apis.quran.views import SearchQuran_v2
from master.apis.sunnah.views import SunnahVerseSearchAPI
from .serializers import *
from .pagination import CustomLimitPagination
from .prayertime import PrayTimes
import requests
from django.db.models import F, Value, CharField
import json
import random
import re

class PrayerTimeAPI(APIView):
    def post(self, request):
        try:
            latitude = request.data["latitude"]
            longitude = request.data["longitude"]
            month = request.data["month"]
            year = request.data["year"]
            url = f"http://api.aladhan.com/v1/calendar?latitude={latitude}&longitude={longitude}&method=2&month={month}&year={year}"
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
        
class SearchQuranAndSunnahAPI(ListAPIView):
    serializer_class = SearchQuranAndSunnahSerializer
    pagination_class = CustomLimitPagination
    
    def get_queryset(self):
        quranic_verses = SearchQuran_v2.get_queryset(self).annotate(verse_type=Value("quran", output_field=CharField()))
        sunnah_verses = SunnahVerseSearchAPI.get_queryset(self).annotate(verse_type=Value("sunnah", output_field=CharField()))
            # Convert both querysets to lists and then combine them
        combined_data = list(quranic_verses) + list(sunnah_verses)
        # random.shuffle(combined_data)
        return combined_data
        
        # return {"sunnah":sunnah_verses, "quran": quranic_verses}

    def _validateSearchText(self, text):
        # removing special Character.
        text2 = re.sub("[$*&^#@!]","",text) 
        if text2 == "":
            return text
            
        text2 = re.sub(" +"," ",text2)
        # removing extra whitespaces.
        return text2 

class OnBoardingScreenAPI(ListAPIView):
    queryset = OnBoardingScreens.objects.all()
    serializer_class = OnBoardingScreenSerializer