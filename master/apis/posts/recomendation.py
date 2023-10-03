from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cdist
import numpy as np
from master.models import *
import json

model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")

class PostRecomender:
    def __init__(self, user, posts, top_n=20) -> None:
        self.user = user
        self.posts = posts
        self.top_n = top_n
        categories = user.categories.all()
        self.prefrence_embeddings = [model.encode(category.name) for category in categories]
        self.post_embeddings = [self._load_embeddings(post.embeddings) for post in posts]

    def _load_embeddings(self, embedding_string):
        return np.array(list(map(float, embedding_string.split())))

    def get_prefered_posts(self):
        distances = cdist(self.prefrence_embeddings, self.post_embeddings, metric="cosine")
        sorted_indices = np.argsort(distances[0])
        top_indices = sorted_indices[:self.top_n]
        prefered_posts = [self.posts[int(indice)] for indice in top_indices]
        return prefered_posts

