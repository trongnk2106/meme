from faissDB import FAISS

from handleMeme import MemeGenerator 
import numpy as np
import pandas as pd



class MemePipeline:
    def __init__(self, faiss_index_path, meme_generator):
        self.faiss = FAISS()
        self.faiss.load_index(faiss_index_path)
        self.meme_generator = meme_generator
        self.df = pd.read_csv("meme_data.csv")

    def query_image_and_caption(self, query, k=2):
        query_embedding = np.array([self.meme_generator.get_embedding(query)]).astype("float32")
        distances, indices = self.faiss.search(query_embedding, k)
        list_of_memes = []
        list_image_path = []
        for i in range(k):
            meme = self.faiss.texts[indices[0][i]]
            list_of_memes.append(meme)
            list_image_path.append(self.df['image_path'][indices[0][i]])
        
        return list_of_memes, list_image_path

    def pipeline(self, query, k=2):
        list_meme = []
        for user_context, image_path in zip(*self.query_image_and_caption(query, k)):
            meme = self.meme_generator.generate_meme(user_context, image_path)
            list_meme.append(meme)
            
        return list_meme

    
if __name__ == "__main__":
    
    user_input = "Meme Title: And Just Like That"
    faiss_index_path = "vectordb.index"
    meme_generator = MemeGenerator()
    meme_pipeline = MemePipeline(faiss_index_path, meme_generator)
    results = meme_pipeline.search_and_generate(user_input, k=2)
