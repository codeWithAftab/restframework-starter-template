# import pandas as pd
# from master.models import *
# import json
# from master.models import Language, Narration, Verse

# def addChapters():
#     df = pd.read_excel("chapters_sheet1.xlsx")
#     for index,row in df.iterrows():
#         chapter_id = row["CHAPTER ID"]
#         translit = row["SURAH TITLE ROMAN"]
#         english_title = row["SURAH MEANING IN ENGLISH"]
#         arabic_title = row["SURAH IN ARABIC"]
#         location = row["LOCATION"]
#         verses = row["VERSES"]
#         verse_timings = row["VERSE TIMINGS"]
#         chapter = Chapter.objects.create(chapter_id=int(chapter_id), translit_name=translit, en_name=english_title, ar_name=arabic_title, origin=location, verse_count=int(verses))
#         print(chapter)



# def create_verse_db(text, language_id):
#     with open("surahfinal_all.json","r+") as f:
#         allendata = json.loads(f.read())
#         language = Language.objects.get(language_id=language_id)
#         style = Narration.objects.get(narration_id=0)
#         chapter_id = 1
#         chapter = Chapter.objects.get(chapter_id=chapter_id)
#         for index, obj in enumerate(allendata["surah_verse_quran"], 1):
#             if chapter_id != int(obj["sura_no"]):
#                 chapter_id = int(obj["sura_no"])
#                 chapter = Chapter.objects.get(chapter_id=int(obj["sura_no"]))

#             try:
#                 verse = Verse(verse_id=index , chapter=chapter, content=obj[text], verse_number=obj["aya_no"], narration=style, language=language)
#                 print(verse)
#                 verse.save()
#             except Exception as e:
#                 print(e)

# def run_for_quran_data():
#     addChapters()
#     create_verse_db("aya_text", 0)
#     create_verse_db("en_text", 1)