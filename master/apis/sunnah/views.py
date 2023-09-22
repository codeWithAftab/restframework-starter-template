from typing import Any
from master.models import SunnahVerse, SunnahBook, SunnahCollection
from rest_framework.generics import ListAPIView
from firebase_auth.authentication import FirebaseAuthentication
from rest_framework.pagination import PageNumberPagination
from .serializers import *
from rest_framework.response import Response
from django.db.models import Prefetch, Q, F
import re

class CustomListAPIView(ListAPIView):
    def __init__(self, **kwargs: Any) -> None:
        self.is_many = True

    def get(self, request, collection_id=None):
        serializer = self.get_serializer(self.get_queryset(), many=self.is_many)
        response = {
            "data": serializer.data
        }
        return Response(response)
    
class SunnahCollectionAPI(CustomListAPIView):
    queryset = SunnahCollection.objects.all()
    serializer_class = SunnahCollectionSerializer


class SunnahBookAPI(CustomListAPIView):
    serializer_class = SunnahBookSerializer

    def get_queryset(self):
        collection_id = self.kwargs["collection_id"]
        return SunnahBook.objects.filter(collection__collection_id=collection_id)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        params = self.request.GET
        context["params"] = params
        return context
    
class SunnahVerseSearchAPI(ListAPIView):
    serializer_class = SunnahVerseSearchSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        collection_id = self.kwargs["collection_id"] if self.kwargs.get("collection_id", None) else self.request.GET["collection_id"] 
        keyword = self.request.GET["keyword"]
        return SunnahVerse.objects.select_related('language','book','collection').filter(
                                Q(collection__collection_id=collection_id),
                                Q(content__icontains=" {0} ".format(keyword)) |
                                Q(content__icontains=" {0}.".format(keyword)) |
                                Q(content__icontains=" {0},".format(keyword)) 
                                )
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        params = self.request.GET
        context["params"] = params
        return context
    
class SunnahBookSearchAPI(ListAPIView):
    serializer_class = SunnahBookSerializer
    
    def get_queryset(self):
        collection_id = self.kwargs["collection_id"]
        keyword = self.request.GET["keyword"]
        return SunnahBook.objects.select_related('collection').filter(
                                Q(collection__collection_id=collection_id),
                                Q(en_name__icontains=keyword)
                                )
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        params = self.request.GET
        context["params"] = params
        return context

