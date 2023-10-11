from master.models import *

def add_quran_source():
    quran_verses = Verse.objects.filter(language_id=1)
    quran_posts = Post.objects.filter(user__uid="quran-ids")
    print(quran_posts)

    for verse, post in zip(quran_verses, quran_posts):
        source = f"{verse.chapter.en_name} : {verse.verse_number}"
        post.source = source
        print(post)
        post.save()

def add_hadith_source():
    hadith_verses = SunnahVerse.objects.filter(collection_id=1)
    hadith_posts = Post.objects.filter(user__uid="hadith-ids")
    print(hadith_posts)

    for verse, post in zip(hadith_verses, hadith_posts):
        source = f"{verse.collection.name} {verse.book.book_id}:{verse.number}"
        post.source = source
        print(post)
        post.save()

def add_books():
    hadith_post = Post.objects.filter(user__uid="hadith-ids")
    quran_post = Post.objects.filter(user__uid="quran-ids")

    hadith_book = IslamicBook.objects.get(book_id=2)
    quran_book = IslamicBook.objects.get(book_id=1)
    
    for post in hadith_post:
        post.book = hadith_book
        print(post)
        post.save()

    for post in quran_post:
        post.book = quran_book
        print(post)
        post.save()
    
