
from qdrant_db_connect import QdrantDBConnection
from handleMeme import MemeGenerator 
import numpy as np
import pandas as pd
from utils import get_embedding, get_description_for_image
from PIL import Image, ImageDraw, ImageFont


class MemePipeline:
    def __init__(self,qdrant_url,vector_emdding_path, meme_generator):
        self.qdrant_client = QdrantDBConnection(url=qdrant_url)
        self.embedding = np.load(vector_emdding_path)
        self.meme_generator = meme_generator
        self.df = get_description_for_image('./meme_data.csv', num_rows=10, get_all=False)
        self.qdrant_client.index_data(self.df, self.embedding)

    def query_image_and_caption(self, query, k=2):
     
        results = self.qdrant_client.search(query, limit=k)
        list_of_memes = []
        list_image_path = []
        for result in results:
            meme_context = result.payload['text']
            image_path = result.payload['name']
            list_of_memes.append(meme_context)
            list_image_path.append(image_path)
        return list_of_memes, list_image_path

    def pipeline(self, query, k=2):
        list_meme = []
        list_of_context_meme, list_image_path = self.query_image_and_caption(query, k)
        for meme_context, image_path in zip(list_of_context_meme, list_image_path):
            image_path = "./images/" + image_path
            meme = self.meme_generator.generate_meme(image_path, meme_context)
            list_meme.append([image_path, meme])
            
        return list_meme



def draw_captions_on_image(image_path, data, output_path="output.jpg"):
    img = Image.open(image_path).convert("RGB")
    draw = ImageDraw.Draw(img)

    for caption in data["captions"]:
        x = caption["x"]
        y = caption["y"]
        text = caption["text"]
        font_size = caption.get("fontSize", 24)
        # Font fallback
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        draw.text((x, y), text, font=font, fill="white", stroke_width=2, stroke_fill="black")

    img.save(output_path)
    img.show()


if __name__ == "__main__":
    
    user_input = "Meme Title: And Just Like That"
    vector_emdding_path = "embeddings.npy"
    meme_generator = MemeGenerator()
    meme_pipeline = MemePipeline("http://103.186.100.39:6333", vector_emdding_path, meme_generator)
    results = meme_pipeline.pipeline(user_input, k=1)
    for idx, result in enumerate(results):
       
        draw_captions_on_image(result[0], result[1], output_path=f"output_meme_{idx}.jpg")