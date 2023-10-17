from django.contrib import admin, messages
from master.models import *
from account.models import CustomUser
from PIL import Image
from django.core.exceptions import ValidationError
from master.forms import OnBoardingScreenAdminForm


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id',"user", "like_counts", "category",'short_content']
    fields = ["user", "category",'source',"tags",'embeddings','en_content','ar_content','like_counts']
    # readonly_fields = ["like_counts"]
    filter_horizontal = ["tags", 'liked_users']

    def short_content(self, obj):
        return obj.en_content


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ['tag_id',"name"]

@admin.register(IslamicBook)
class IslamicBookAdmin(admin.ModelAdmin):
    list_display = ["book_id",'en_name',"ar_name", 'cover_image']
    fields = ["book_id",'en_name',"ar_name", 'cover_image', 'is_available']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'embeddings', 'description']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    fields = ["user","post",'content']
    readonly_fields = ["like_counts"]
    filter_horizontal = ['liked_users']

@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    fields = [ "user","comment","tags",'content']
    readonly_fields = ["like_counts"]
    filter_horizontal = ['liked_users']


# class OnBoardingScreenAdmin(admin.ModelAdmin):
#     form = OnBoardingScreenAdminForm

admin.site.register(Chapter)
admin.site.register(Verse)
admin.site.register(Language)
admin.site.register(QuranJuz)
admin.site.register(Narration)
admin.site.register(SunnahCollection)
admin.site.register(SunnahBook)
admin.site.register(SunnahVerse)
admin.site.register(PostView)
admin.site.register(OnBoardingScreens)