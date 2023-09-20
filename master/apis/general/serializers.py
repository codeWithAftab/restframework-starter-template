from rest_framework import serializers
from master.models import Post, Comment, Reply, Tag, Category, LikeableModel
from account.api.serializers import UserSerializer_v2, UserSerializer

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

    class Meta:
        model = Post
        fields = ['id','user','source','category','ar_content',"en_content",'like_counts','liked_users','tags','created_on','updated_on']

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
        

