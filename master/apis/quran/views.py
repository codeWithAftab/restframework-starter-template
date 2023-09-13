from rest_framework.generics import ListAPIView
from firebase_auth.authentication import FirebaseAuthentication
from rest_framework.pagination import PageNumberPagination
from master.models import Chapter
from .serializers import *
from rest_framework.response import Response
from django.db.models import Prefetch, Q, F
import re


class QuranChaptersApi(ListAPIView):
    serializer_class = ChapterSerializer

    def get_queryset(self):
        chapter_id = self.kwargs.get("chapter_id")
        if chapter_id:
            self.is_many = False
            return Chapter.objects.get(chapter_id=chapter_id)
        
        self.is_many = True
        return Chapter.objects.all()
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        params = self.request.GET
        context["params"] = params
        return context
    
    def get(self, request, chapter_id=None):
        serializer = self.get_serializer(self.get_queryset(), many=self.is_many)
        response = {
            "data": serializer.data
        }
        return Response(response)

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
    pagination_class = PageNumberPagination

    def get_queryset(self):
        keyword = self._validateSearchText(self.request.GET["keyword"])
        # regex = r'\b[A-Z]{0}*\b'.format(keyword)
        # print(regex)
        chapters = Verse.objects.select_related('chapter','language').filter(
            Q(content__icontains=" {0} ".format(keyword)) |
            # Q(content__regex=r'\b[A-Z]{0}*\b'.format(keyword)) |
            Q(content__icontains=" {0}.".format(keyword)) |
            Q(content__icontains=" {0},".format(keyword)) 
            )
        return chapters
    
    def get_serializer_context(self, *args, **kwargs):
        context = super().get_serializer_context()
        context["params"] = self.request.GET
        return context
    
        
    def _validateSearchText(self, text):
        text2 = re.sub("[$*&^#@!]","",text) # removing special Character.
        if text2 == "":
            return text
            
        text2 = re.sub(" +"," ",text2)
        return text2 # removing extra whitespaces.
    


class LanguagesListApi(ListAPIView):
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()
    
    def get(self, request):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        response = {
            "data": serializer.data
        }
        return Response(response)

