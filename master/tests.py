from django.test import TestCase

# Create your tests here.
from master.models import Verse, Post, CustomUser, Category

def create_post():
    user = CustomUser.objects.first()
    category = Category.objects.get(category_id=3)
    verses_english = Verse.objects.filter(language__language_id=1)
    verses_arabic = Verse.objects.filter(language__language_id=0)
    print(verses_arabic)
    for (en_verse, ar_verse) in zip(verses_english, verses_arabic):
        post = Post.objects.create(
                        user=user,
                        category=category,
                        source=1,
                        en_content=en_verse.content,
                        ar_content=ar_verse.content
                    )   

        print(post)