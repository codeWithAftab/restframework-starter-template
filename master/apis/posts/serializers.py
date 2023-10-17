from rest_framework import serializers
from master.models import Post, Comment, Reply, Tag, Category, LikeableModel, PostView, IslamicBook
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
    # username = serializers.CharField(source="user.username")
    book_name = serializers.CharField(source="book.en_name")
    book_cover = serializers.SerializerMethodField()
    liked_by_current_user = serializers.SerializerMethodField()
    liked_users = serializers.SerializerMethodField()
    views_count = serializers.SerializerMethodField()
    comment_count = serializers.SerializerMethodField()
    is_audio_available = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'source', "book_name", "book_cover",  'ar_content', "en_content", 'like_counts', 'comment_count',
                  'is_audio_available', 'views_count', 'liked_by_current_user', 'liked_users', 'is_verified', 'created_on', 'updated_on']

    def get_views_count(self, obj):
        count = obj.views.aggregate(Sum('count'))["count__sum"]
        if count:
            return count
        return 0
    
    def get_liked_by_current_user(self, obj):
        request = self.context["request"]
        user = request.user
        if user in obj.liked_users.all():
            return True
        return False
    
    # def get_user(self, obj):
    #     return UserSerializer_v2(obj.user).data
    
    def get_book_cover(self, obj):
        request = self.context.get('request')
        if request:
            image_url = obj.book.cover_image.url
            if image_url:
                return request.build_absolute_uri(image_url)
            return None
        return "pass request in context"

    def get_is_audio_available(self, obj):
        return False

    def get_comment_count(self, obj):
        return len(obj.comments.all())
    
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


class PostViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostView
        fields = "__all__"

class IslamicBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = IslamicBook
        fields = "__all__"



# class MCQOptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = MCQOption
#         fields = "__all__"

# class QuestionSerializer(serializers.ModelSerializer):
#     options = serializers.SerializerMethodField()

#     class Meta:
#         model = Question
#         fields = ["id", "question", "options"]

#     def get_options(self, obj):
#         mcqs = obj.mcqs.all()
#         serializer = MCQOptionSerializer(mcqs, many=True)
#         return serializer.data

# class UserQuizSerializer(serializers.ModelSerializer):
#     questions = serializers.SerializerMethodField()

#     class Meta:
#         model = UserQuiz
#         fields = "__all__"

#     def get_questions(self, obj):
#         serializer = QuestionSerializer(obj.questions.all(), many=True)
#         return serializer.data
