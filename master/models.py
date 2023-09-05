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
        ("0","Al-Quran"),
        ("1", "Al-Hadith")
    )
    source = models.CharField(max_length=122, null=True, choices=SOURCES)
    ar_content = models.TextField(null=True, blank=True)
    en_content = models.TextField(null=True, blank=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"Post {self.id}"

        
class Comment(LikeableModel, models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user} : {self.post}"
    

class Reply(LikeableModel, models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
        
    class Meta:
        verbose_name = 'Reply'
        verbose_name_plural = 'Replies'

    def __str__(self) -> str:
        return f"{self.user} : {self.post}"

    

    
    
