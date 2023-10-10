from rest_framework import serializers
from master.models import Post, Comment, Reply, Tag, Category, LikeableModel, PostView
from account.api.serializers import UserSerializer_v2, UserSerializer
from django.db.models import Sum

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"

class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer_v2()
    liked_users = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = "__all__"

    def get_liked_users(self, obj):
        show_liked_users = self.context.get('show_liked_users', False)
        if not show_liked_users:
            return None
        
        users_serializer = UserSerializer_v2(obj.get_liked_users(), many=True)
        return users_serializer.data
    
    def to_representation(self, instance):
        # Get the original representation using the parent class method
        representation = super().to_representation(instance)
        
        # Check if weeks should be included based on the context
        show_liked_users = self.context.get("show_liked_users", False)
  
        if not show_liked_users:
            representation.pop("liked_users")

        return representation
        


class ReplySerializer(serializers.ModelSerializer):
    user = UserSerializer_v2()
    
    class Meta:
        model = Reply
        fields = "__all__"

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeableModel
        field = "__all__"

class PostsSerializer(serializers.ModelSerializer):
    liked_users = serializers.SerializerMethodField()
    tags = TagSerializer(many=True)
    source = serializers.SerializerMethodField()
    views_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    is_audio_available = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id','user','source','category','ar_content',"en_content",'like_counts', 'comment_count', 'is_audio_available', 'liked_users','views_count','tags','created_on','updated_on']

    def get_views_count(self, obj):
        count = obj.views.aggregate(Sum('count'))["count__sum"]
        if count:
            return count
        return 0
    
    def get_is_audio_available(self, obj):
        return False
    
    def get_comment_count(self, obj):
        return len(obj.comments.all())

    def get_source(self, obj):
        if obj.source == 1:
            return "Al-Quran"
        return "Al-Hadith"
    
    def get_liked_users(self, obj):
        show_liked_users = self.context.get('show_liked_users', False)
        if not show_liked_users:
            return None
        
        users_serializer = UserSerializer(obj.get_liked_users(), many=True)
        return users_serializer.data
    
    def to_representation(self, instance):
        # Get the original representation using the parent class method
        representation = super().to_representation(instance)
        
        # Check if weeks should be included based on the context
        show_liked_users = self.context.get("show_liked_users", False)
  
        if not show_liked_users:
            representation.pop("liked_users")

        return representation
        
class PostViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostView
        fields = "__all__"

