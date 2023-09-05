from django.contrib import admin
from master.models import Category, Tag, Post, Reply, Comment
from account.models import CustomUser

# Register your models here.
admin.site.register(CustomUser)
# admin.site.register(Category)
# admin.site.register(Tag)
# # admin.site.register(Post)
# admin.site.register(Reply)

# class LikeableModelAdmin(admin.ModelAdmin):
#     list_display = ('like_counts',)  # Add other fields you want to display
#     readonly_fields = ('like_counts',)  # Make the field read-only


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['id',"user", "like_counts", "category",'short_content']
    fields = ["user", "category",'source',"tags",'en_content','ar_content','like_counts']
    # readonly_fields = ["like_counts"]
    filter_horizontal = ["tags", 'liked_users']

    def short_content(self, obj):
        return obj.en_content


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    fields = ['tag_id',"name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    fields = ["category_id", 'name', 'description']


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