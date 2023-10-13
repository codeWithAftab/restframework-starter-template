from rest_framework.generics import ListAPIView
from firebase_auth.authentication import FirebaseAuthentication
from rest_framework.pagination import PageNumberPagination
from master.models import Chapter
from .serializers import *
from rest_framework.response import Response
from django.db.models import Prefetch, Q, F
from master.utils import compress_data
from django.http import HttpResponse
import re


class QuranChaptersApi(ListAPIView):
    serializer_class = ChapterSerializer

    def get_queryset(self):
        chapter_id = self.kwargs.get("chapter_id")
        if chapter_id:
            self.is_many = False
            return Chapter.objects.get(chapter_id=chapter_id)
        
        self.is_many = True
        return Chapter.objects.prefetch_related('verses').all()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        params = self.request.GET
        context["params"] = params
        return context
    
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        # print(compressed_data)
        response = {
            "data": serializer.data
        }
        compressed_data = compress_data(response)
        response = HttpResponse(compressed_data, content_type='application/json')
        response['Content-Encoding'] = 'gzip'
        return response

class SearchQuran(ListAPIView):
    serializer_class = ChapterSearchSerializer

    def get_queryset(self):
        params = self.request.GET
        chapters = Chapter.objects.filter( Q(en_name__icontains=params["keyword"]) |
                                           Q(translit_name__icontains=params["keyword"]) |
                                           Q(origin__icontains=params["keyword"]) |
                                           Q(verses__content__icontains=params["keyword"])
                                        ).distinct()
        return chapters
    
    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context()
        context["params"] = self.request.GET
        return context
    
    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        response = {
            "counts": len(self.get_queryset()),
            "data": serializer.data
        }
        return Response(response)

class SearchQuran_v2(ListAPIView):
    serializer_class = ChapterSearchSerializer_v2   
    # pagination_class = PageNumberPagination

    def get_queryset(self):
        keyword = self._validateSearchText(self.request.GET["keyword"])
        chapters = Verse.objects.select_related('chapter','language').filter(
            Q(content__icontains=" {0} ".format(keyword)) |
            Q(content__icontains=" {0}.".format(keyword)) |
            Q(content__icontains=" {0},".format(keyword)) 
            )
        return chapters
    
    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context()
        context["params"] = self.request.GET
        return context
    
        
    def _validateSearchText(self, text):
        # removing special Character.
        text2 = re.sub("[$*&^#@!]","",text) 
        if text2 == "":
            return text
            
        text2 = re.sub(" +"," ",text2)
        # removing extra whitespaces.
        return text2 
    

class LanguagesListApi(ListAPIView):
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()
    
    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        response = {
            "data": serializer.data
        }
        return Response(response)


