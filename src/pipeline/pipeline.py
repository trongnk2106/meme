
from src.database.connection import QdrantDBConnection
from src.pipeline.meme_generator import MemeGenerator 
import numpy as np
import pandas as pd
from src.utils.utils import get_embedding, get_description_for_image, download_image
from PIL import Image, ImageDraw, ImageFont
from src.utils.DrawMeme import draw_bbox_pillow

class MemePipeline:
    def __init__(self,qdrant_url, meme_generator, vector_db_collection="meme_collection"):
        self.qdrant_client = QdrantDBConnection(url=qdrant_url, collection_name=vector_db_collection)
        self.meme_generator = meme_generator

    def query_image_and_caption(self, query, k=2):
        results = self.qdrant_client.search(query, limit=k)
        list_of_memes = []
        list_images_urls = []
        list_image_names = []
        for result in results:
            meme_context = result.payload['text']
            image_name = result.payload['name']
            image_url = result.payload['image_path']
            list_of_memes.append(meme_context)
            list_image_names.append(image_name)
            list_images_urls.append(image_url)
        return list_of_memes, list_image_names, list_images_urls
    
    def pipeline(self, query, k=2):
        list_meme = []
        list_of_memes, list_image_names, list_images_urls = self.query_image_and_caption(query, k)

        for meme_context, image_url in zip(list_of_memes, list_images_urls):

            meme = self.meme_generator.generate_meme(
                image_url = image_url,
                user_context = query, 
                image_description = meme_context)
            list_meme.append(meme)

        return list_meme

    def draw_meme(self, image, meme_text, bbox=None):
        draw_bbox_pillow()



