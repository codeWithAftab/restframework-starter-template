from django.db import models
from account.models import CustomUser

class Category(models.Model):
    category_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=122)
    description = models.TextField()

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self) -> str:
        return f"{self.category_id} : {self.name}"

        

class Tag(models.Model):
    tag_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=122)
    description = models.TextField()

    def __str__(self) -> str:
        return f"{self.tag_id} : {self.name}"

class LikeableModel(models.Model):
    like_counts = models.IntegerField(default=0)
    liked_users = models.ManyToManyField(CustomUser)
       
    def get_liked_users(self):
        return self.liked_users.all()
    
    def update_like_counts(self):
        '''
        it will use for updating realtime like_counts using the liked_users.
        24-08-2023 : currently we are not using this method. only using the liked and disliked function 
                    to updating the likes_count by 1 because i am assuming
                    'like_counts' not create inconsistency in database.
                    In future if it creates inconsistency in database we can
                    use this method in liked and disliked methods to update the
                    realtime likes.
        '''
        users = self.get_liked_users()
        self.like_counts = len(users)
        self.save()

    def liked(self, user):
        if user in self.get_liked_users():
            return True
        return False

    def increase_like(self, user):
        self.liked_users.add(user)
        self.like_counts += 1
        self.save()

    def decrease_like(self, user):
        self.liked_users.remove(user)
        self.like_counts -= 1
        self.save()

    class Meta:
        abstract = True

class Post(LikeableModel, models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='posts')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, null=True, blank=True)
    SOURCES = (
        (0, "Al-Quran"),
        (1, "Al-Hadith")
    )
    source = models.IntegerField(null=True, choices=SOURCES)
    ar_content = models.TextField(null=True, blank=True)
    en_content = models.TextField(null=True, blank=True)
    # comment_count = models.PositiveIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Post {self.id}"
    
    def get_comments(self):
        return self.comments.all()
    
    def do_comment(self, user, content):
        return Comment.objects.create(user=user, post=self, content=content)
    
    def remove_comment(self, user, comment_id):
        comment = self.comments.get(user=user, id=comment_id, is_removed=False)
        comment.is_removed = True
        comment.save()

        
class Comment(LikeableModel, models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    is_removed = models.BooleanField(default=False)
    reply_count = models.PositiveIntegerField(default=0)
    content = models.TextField()
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user} : {self.post}"
    
    def increase_reply_count(self):
        self.reply_count += 1
        self.save()

    def decrease_reply_count(self):
        self.reply_count -= 1
        self.save()

    def do_reply(self, user, content):
        reply =  Reply.objects.create(comment=self, user=user, content=content)
        self.increase_reply_count()
        return reply
     
    def remove_reply(self, user, reply_id):
        reply = self.replies.get(user=user, id=reply_id, is_removed=False)
        self.decrease_reply_count()
        reply.is_removed = True
        reply.save()
    
    def get_replies(self):
        return self.replies.all()

class Reply(LikeableModel, models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='replies')
    is_removed = models.BooleanField(default=False)
    content = models.TextField()
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'

    def __str__(self) -> str:
        return f"{self.user} : {self.comment}"


class Narration(models.Model):
    narration_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100, null=True, blank= True)
    # image = models.ImageField(upload_to=nameFile,null=True, blank=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name
    
class Chapter(models.Model):
    chapter_id = models.IntegerField(unique=True)
    en_name = models.CharField(max_length=122, verbose_name="English Name")
    ar_name = models.CharField(max_length=122, verbose_name="Arabic Name")
    translit_name = models.CharField(max_length=122, verbose_name="Transliteration")
    ORIGIN_CHOICES = (
        ("Makka","Makkiyyah"),
        ("Medina","Madaniyyah"),
    )
    origin = models.CharField(max_length=122, choices=ORIGIN_CHOICES)
    verse_count = models.IntegerField()

    class Meta:
        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"

class QuranJuz(models.Model):
    juz_id = models.IntegerField(unique=True)
    en_name = models.CharField(max_length=122, null=True, verbose_name="English Name")
    ar_name = models.CharField(max_length=122, null=True, verbose_name="Arabic Name")
    ur_name = models.CharField(max_length=122, null=True, verbose_name="Arabic Name")
    translit_name = models.CharField(max_length=122,null=True, verbose_name="Transliteration")
    verse_count = models.IntegerField(null=True,blank=True)

    start_chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='juz_start_chapters',null=True,blank=True,default=None)
    start_verse_number = models.IntegerField(null=True,blank=True)

    end_chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='juz_end_chapters',null=True,blank=True,default=None)
    end_verse_number = models.IntegerField(null=True,blank=True)

    def __str__(self) -> str:
        return f"{self.juz_id} : Name : {self.en_name}"


class Language(models.Model):
    language_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=122)
    code = models.CharField(max_length=122)
    is_available = models.BooleanField(default=True)


class Verse(models.Model):
    verse_id = models.IntegerField()
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name="verses")
    narration = models.ForeignKey(Narration, on_delete=models.CASCADE, null=True, blank=True, related_name='narration_style')
    juz = models.ForeignKey(QuranJuz, on_delete=models.CASCADE, null=True, blank=True, default=None, related_name="verse_data")
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="verses")
    verse_number = models.PositiveIntegerField()
    content = models.TextField()

    def __str__(self) -> str:
        return f"Verse {self.chapter.chapter_id} : {self.verse_number}"
    
class ChapterAudio(models.Model):
    chapter = models.OneToOneField(Chapter, on_delete=models.CASCADE, related_name="audio")
    file = models.FileField(upload_to="")


# hadith models

def upload_hadiths_collection(instance, filename):
    # file will be uploaded to MEDIA_ROOT / audio/chapters/{reciter_name}/filename.mp3
    return f'hadith/collection/{filename}'


# models for hadis features
class SunnahCollection(models.Model):
    collection_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=122, null=True, blank=True)
    image = models.ImageField(upload_to=upload_hadiths_collection, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_available = models.BooleanField(default=True)

    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
  
    def __str__(self):
        return f"{self.name} "


class SunnahBook(models.Model):
    collection = models.ForeignKey(SunnahCollection,on_delete=models.CASCADE,related_name="books")
    book_id = models.IntegerField(null=True, blank=True)
    volume_id = models.IntegerField(null=True, blank=True)
    en_name = models.CharField(max_length=134, null=True, blank=True)
    ar_name = models.CharField(max_length=134, null=True, blank=True)
    is_available = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('collection', 'book_id')

    def __str__(self):
        return f"{self.book_id}. {self.en_name}"

class SunnahVerse(models.Model):
    collection = models.ForeignKey(SunnahCollection, on_delete=models.CASCADE, related_name="verses")
    hadith_id = models.IntegerField(null=True)
    book = models.ForeignKey(SunnahBook, on_delete=models.CASCADE, related_name="verses")
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name="sunnah_verses")
    number = models.IntegerField(null=True, blank=True)
    narrated_by = models.CharField(max_length=132)
    source = models.CharField(max_length=132) 
    content = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('book', 'language', 'number')

    def __str__(self):
        return f"{self.collection} {self.book} "

    def save(self, *args, **kwargs):
        try:
            self._change_update_status_of_book()
        except:
            pass
        super(SunnahVerse, self).save(*args, **kwargs)
    
    def _change_update_status_of_book(self):
        self.book.updated_on = self.updated_on
        self.book.save()


# class HadithBookmark(models.Model):
#     user = models.ForeignKey('accounts.CustomUser', on_delete=models.CASCADE, related_name='hadith_bookmarks')
#     hadith = models.ForeignKey(HadithData, on_delete=models.CASCADE, related_name='bookmarks')
#     created_at = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         unique_together = ('user', 'hadith')