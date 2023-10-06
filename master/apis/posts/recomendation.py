from sentence_transformers import SentenceTransformer
from scipy.spatial.distance import cdist
import numpy as np
from master.models import *
import json

model = SentenceTransformer("sentence-transformers/paraphrase-MiniLM-L6-v2")

class PostRecomender:
    def __init__(self, user, posts, top_n=100) -> None:
        self.user = user
        self.posts = posts
        self.top_n = top_n
    
    def _load_embeddings(self, embedding_string):
        return np.array(list(map(float, embedding_string.split())))
    
    def _get_user_prefrences_embeddings(self): 
        categories = self.user.categories.all()
        return [model.encode(category.name) for category in categories]

    def _get_posts_embeddings(self): 
        return [self._load_embeddings(post.embeddings) for post in self.posts]
    
    def get_prefered_posts(self):
        distances = cdist(self._get_user_prefrences_embeddings(), self._get_posts_embeddings(), metric="cosine")
        sorted_indices = np.argsort(distances[0])
        top_indices = sorted_indices[:self.top_n]
        prefered_posts = [self.posts[int(indice)] for indice in top_indices]
        return prefered_posts

