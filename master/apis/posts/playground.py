# from sentence_transformers import SentenceTransformer
# from scipy.spatial.distance import cdist
# import numpy as np
# from master.models import *
# import json

# model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")
# # categories = Category.objects.all()

# posts = Post.objects.all().order_by("id")
# categories = ["War", "Moral Values", "Personal Growth"]
# # # posts = [
# #     "Gratitude is the key to contentment. Let's take a moment today to thank Allah for all the blessings we have. #Alhamdulillah 🙏🏼❤️",
# #     "In the Name of Allah—the Most Compassionate, Most Merciful.",
# #     "All praise is for Allah—Lord of all worlds,",
# #     "the Most Compassionate, Most Merciful,",
# #     "Master of the Day of Judgment.",
# #     "You ˹alone˺ we worship and You ˹alone˺ we ask for help.",
# #     "Guide us along the Straight Path,",
# #     "the Path of those You have blessed—not those You are displeased with, or those who are astray.",
# #     "Alif-Lãm-Mĩm.",
# #     "This is the Book! There is no doubt about it —a guide for those mindful ˹of Allah˺,",
# #     "who believe in the unseen,  establish prayer, and donate from what We have provided for them,",
# #     "and who believe in what has been revealed to you ˹O Prophet˺  and what was revealed before you, and have sure faith in the Hereafter.",
# #     "It is they who are ˹truly˺ guided by their Lord, and it is they who will be successful.",
# #     "As for those who persist in disbelief, it is the same whether you warn them or not—they will never believe.",
# #     "Allah has sealed their hearts and their hearing, and their sight is covered. They will suffer a tremendous punishment.",
# #     "And there are some who say, “We believe in Allah and the Last Day,” yet they are not ˹true˺ believers.",
# #     "They seek to deceive Allah and the believers, yet they only deceive themselves, but they fail to perceive it.",
# #     "There is sickness in their hearts, and Allah ˹only˺ lets their sickness increase. They will suffer a painful punishment for their lies.",
# #     "When they are told, “Do not spread corruption in the land,” they reply, “We are only peace-makers!”",
# #     "Indeed, it is they who are the corruptors, but they fail to perceive it."
# # ]

# def load_embeddings(embedding_string):
#     return np.array(list(map(float, embedding_string.split())))

# Categories = [
#     {
#       "CategoryName": "Ritual Purification and Prayers",
#       "Chapters": [
#         "Ablutions (Wudu')",
#         "Bathing (Ghusl)",
#         "Rubbing hands and feet with dust (Tayammum)",
#         "Prayers (Salat)",
#         "Times of the Prayers",
#         "Shortening the Prayers (At-Taqseer)",
#         "Forgetfulness in Prayer"
#       ]
#     },
#     {
#       "CategoryName": "Islamic Festivals and Special Prayers",
#       "Chapters": [
#         "The Two Festivals (Eids)",
#         "Friday Prayer",
#         "Witr Prayer",
#         "Invoking Allah for Rain (Istisqaa)"
#       ]
#     },
#     {
#       "CategoryName": "Celestial Events and Religious Acts",
#       "Chapters": [
#         "Eclipses",
#         "Prostration During Recital of Qur'an",
#         "Virtues of the Night of Qadr"
#       ]
#     },
#     {
#       "CategoryName": "Pilgrimage and Travel",
#       "Chapters": [
#         "Hajj (Pilgrimage)",
#         "`Umrah (Minor pilgrimage)",
#         "Pilgrims Prevented from Completing the Pilgrimage",
#         "Penalty of Hunting while on Pilgrimage"
#       ]
#     },
#     {
#       "CategoryName": "Financial Transactions and Trade",
#       "Chapters": [
#         "Sales and Trade",
#         "Sales in which a Price is paid for Goods to be Delivered Later (As-Salam)",
#         "Shuf'a",
#         "Hiring",
#         "Transferance of a Debt from One Person to Another (Al-Hawaala)",
#         "Kafalah",
#         "Representation, Authorization, Business by Proxy"
#       ]
#     },
#     {
#       "CategoryName": "Agriculture and Land Use",
#       "Chapters": [
#         "Agriculture",
#         "Distribution of Water"
#       ]
#     },
#     {
#       "CategoryName": "Economic and Legal Matters",
#       "Chapters": [
#         "Loans, Payment of Loans, Freezing of Property, Bankruptcy",
#         "Khusoomaat"
#       ]
#     },
#     {
#       "CategoryName": "Lost and Found",
#       "Chapters": [
#         "Lost Things Picked up by Someone (Luqatah)"
#       ]
#     },
#     {
#       "CategoryName": "Social and Ethical Guidelines",
#       "Chapters": [
#         "Oppressions",
#         "Peacemaking",
#         "Conditions"
#       ]
#     },
#     {
#       "CategoryName": "Inheritance and Financial Responsibilities",
#       "Chapters": [
#         "Obligatory Charity Tax (Zakat)",
#         "Laws of Inheritance (Al-Faraa'id)",
#         "Blood Money (Ad-Diyat)",
#         "Support for the Family"
#       ]
#     },
#     {
#       "CategoryName": "Marriage and Family",
#       "Chapters": [
#         "Wedlock, Marriage (Nikaah)",
#         "Divorce",
#         "Sacrifice on Occasion of Birth (`Aqiqa)"
#       ]
#     },
#     {
#       "CategoryName": "Food, Drink, and Medicine",
#       "Chapters": [
#         "Food, Meals",
#         "Hunting, Slaughtering",
#         "Al-Adha Festival Sacrifice (Adaahi)",
#         "Drinks",
#         "Patients",
#         "Medicine"
#       ]
#     },
#     {
#       "CategoryName": "Clothing and Dress Code",
#       "Chapters": [
#         "Dress"
#       ]
#     },
#     {
#       "CategoryName": "Social Etiquette and Behavior",
#       "Chapters": [
#         "Good Manners and Form (Al-Adab)",
#         "Asking Permission",
#         "Holding Fast to the Qur'an and Sunnah"
#       ]
#     },
#     {
#       "CategoryName": "Belief and Faith",
#       "Chapters": [
#         "Belief",
#         "Oneness, Uniqueness of Allah (Tawheed)"
#       ]
#     },
#     {
#       "CategoryName": "Knowledge and Education",
#       "Chapters": [
#         "Knowledge"
#       ]
#     },
#     {
#       "CategoryName": "Women's Health and Hygiene",
#       "Chapters": [
#         "Menstrual Periods"
#       ]
#     },
#     {
#       "CategoryName": "Islamic Legal and Judicial Matters",
#       "Chapters": [
#         "Judgments (Ahkaam)"
#       ]
#     },
#     {
#       "CategoryName": "Supplications and Spiritual Practices",
#       "Chapters": [
#         "Invocations",
#         "To make the Heart Tender (Ar-Riqaq)"
#       ]
#     },
#     {
#       "CategoryName": "Prophets, Companions, and Islamic History",
#       "Chapters": [
#         "Beginning of Creation",
#         "Prophets",
#         "Virtues and Merits of the Prophet (pbuh) and his Companions",
#         "Companions of the Prophet",
#         "Merits of the Helpers in Madinah (Ansaar)",
#         "Military Expeditions led by the Prophet (pbuh) (Al-Maghaazi)",
#         "Prophetic Commentary on the Qur'an (Tafseer of the Prophet (pbuh))"
#       ]
#     },
#     {
#       "CategoryName": "Miscellaneous and Special Cases",
#       "Chapters": [
#         "Fear Prayer",
#         "Funerals (Al-Janaa'iz)",
#         "Call to Prayers (Adhaan)",
#         "Virtues of Madinah",
#         "Actions while Praying",
#         "Forgetfulness in Prayer",
#         "Representation, Authorization, Business by Proxy",
#         "Interpretation of Dreams",
#         "Afflictions and the End of the World",
#         "Wishes",
#         "Accepting Information Given by a Truthful Person",
#         "Oaths and Vows",
#         "Expiation for Unfulfilled Oaths",
#         "Apostates",
#         "(Statements made under) Coercion",
#         "Tricks"
#       ]
#     }
#   ]


# def create_post_embeddings():
#     posts = Post.objects.all()
#     for post in posts:
#         embedding = model.encode(post.en_content)
#         print(embedding)
#         embedding_str = str(embedding).replace('\n', ' ').strip()
#         embedding_str = embedding_str.strip('[]')
#         post.embeddings = embedding_str
#         post.save()
#         print(post)

def create_categories():
    for cat in Categories:
        Category.objects.create(name=cat["CategoryName"])


# def get_prefered_posts():
    prefrence_embeddings = [model.encode(category) for category in categories]
    post_embeddings = [load_embeddings(post.embeddings) for post in posts]
    distances = cdist(
           prefrence_embeddings, post_embeddings, metric="cosine"
       )
    
    print(distances)

    sorted_indices = np.argsort(distances[0])
    print(sorted_indices)

    # Define the number of top indices you want to select (e.g., top_n)
    top_n = 10

    # Select the top N indices
    top_indices = sorted_indices[:top_n]

    print(top_indices)
    for indice in top_indices:
        print("----HERE-----")
        print(int(indice))
        print(posts[int(indice)].en_content)

