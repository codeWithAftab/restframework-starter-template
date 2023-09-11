from rest_framework import serializers
from master.models import *
from django.db.models import F



class QuranicVerseSerializer(serializers.ModelSerializer):
    verse_key = serializers.SerializerMethodField()
    language_id = serializers.IntegerField(source="languageid")
    #  = serializers.IntegerField("languageid")
    class Meta:
        model = Verse
        fields = ['language_id','verse_key','verse_number',"content"]

    def get_verse_key(self, obj):
        return str(f"{obj.chapter.chapter_id}:{obj.verse_number}")
    
    
class ChapterSerializer(serializers.ModelSerializer):
    verses = serializers.SerializerMethodField()
    class Meta:
        model = Chapter
        fields = ['chapter_id','en_name','ar_name','translit_name','origin','verse_count',"verses"]
    
    def get_verses(self, obj):
        params = self.context["params"]
        if params.get("show_verse", False):
            language_id = params.get("language_id", 0) 
            verses = obj.verses.filter(language__language_id=language_id).annotate(languageid=F("language__language_id"))
            verse_serializer = QuranicVerseSerializer(verses, many=True)
            return verse_serializer.data
        
        return None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        params = self.context["params"]
        if not params.get("show_verse", False):
            representation.pop('verses')

        return representation
        
class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ["language_id", "name", "code"]