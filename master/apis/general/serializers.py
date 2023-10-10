from master.models import Verse, SunnahVerse, OnBoardingScreens
from rest_framework import serializers
from master.apis.quran.serializers import QuranicVerseSerializer
from master.apis.sunnah.serializers import SunnahVerseSearchSerializer


class SearchQuranAndSunnahSerializer(serializers.Serializer):
    # Define the fields you want to include in the search results
    # # These fields should match the relevant fields in both models

    collection_id = serializers.IntegerField(default=None, source="collection.collection_id")
    book_id = serializers.IntegerField(default=None, source="book.book_id")
    ar_name = serializers.CharField(default=None, source="book.ar_name")
    en_name = serializers.CharField(default=None, source="book.en_name")
    
    verse_key = serializers.SerializerMethodField()
    language_id = serializers.IntegerField(source="language.language_id")
    verse_type = serializers.CharField()
    verse_number = serializers.IntegerField(default=None)

    content = serializers.CharField(default=None)

    
    def get_verse_key(self, obj):
        if isinstance(obj, Verse):
            return str(f"{obj.chapter.chapter_id}:{obj.verse_number}")
        return None

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if representation["verse_type"] == "quran":
            representation.pop('collection_id', None)
            representation.pop('en_name', None)
            representation.pop('book_id', None)
            representation.pop('ar_name', None)
            return representation
        
        representation.pop('verse_number', None)
        representation.pop('verse_key', None)
        return representation

class OnBoardingScreenSerializer(serializers.ModelSerializer):
    class Meta:
        model = OnBoardingScreens
        fields = "__all__"
