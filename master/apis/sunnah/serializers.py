from master.models import SunnahBook, SunnahCollection, SunnahVerse
from rest_framework import serializers


class SunnahCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SunnahCollection
        fields = ['collection_id', 'name', 'image', 'description', 'is_available']

class SunnahBookSerializer(serializers.ModelSerializer):
    verses = serializers.SerializerMethodField()
    class Meta:
        model = SunnahBook
        fields = ['id','collection','book_id','volume_id','en_name','ar_name','is_available','verses']

    def get_verses(self, obj):
        params = self.context["params"]
        if params.get("show_verse", False):
            language_id = params.get("language_id", 1) 
            verses = obj.verses.select_related("language").filter(language__language_id=language_id)
            verse_serializer = SunnahVerseSerializer(verses, many=True)
            return verse_serializer.data
        
        return None
    
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        params = self.context["params"]
        if not params.get("show_verse", False):
            representation.pop('verses')

        return representation

class SunnahVerseSerializer(serializers.ModelSerializer):
    language_id = serializers.IntegerField(source="language.language_id")

    class Meta:
        model = SunnahVerse
        fields = ['id','hadith_id','language_id','number','narrated_by','source','content']
    
class SunnahVerseSearchSerializer(serializers.ModelSerializer):
    language_id = serializers.IntegerField(source="language.language_id")
    collection_id = serializers.IntegerField(source="collection.collection_id")
    book_id = serializers.IntegerField(source="book.book_id")
    en_name = serializers.CharField(source="book.en_name")
    ar_name = serializers.CharField(source="book.ar_name")

    class Meta:
        model = SunnahVerse
        fields = ['collection_id','book_id','language_id', 'en_name','ar_name','number','narrated_by','source','content']
    





