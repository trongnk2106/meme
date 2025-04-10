import faiss
import numpy as np
import pandas as pd
from embeddingService import get_embedding


def load_data(csv_path): 
    df = pd.read_csv(csv_path)
    # select 10 first rows with loc
    df = df.loc[:10]
    sentence_full = "Meme Title: " + df['meme_text'] + "\nImage Description: " + df['description']
    return sentence_full.tolist()

class FAISS: 
    
    def text2embedding(self, texts):
        self.embeddings = [get_embedding(text) for text in texts]
        self.embedding_dim = len(self.embeddings[0])
        self.embeddings = np.array(self.embeddings).astype("float32")
    
    def indexing(self, texts): 
        self.text2embedding(texts)
        self.index = faiss.IndexFlatL2(self.embedding_dim)
        self.index.add(self.embeddings)

    def save_index(self, index_path): 
        faiss.write_index(self.index, index_path)
        
    def load_index(self, index_path): 
        self.index = faiss.read_index(index_path)   
        
    def search(self, query_embedding, k=2): 
        distances, indices = self.index.search(query_embedding, k)
        return distances, indices
    
if __name__ == "__main__":

    full_sentences = load_data("meme_data.csv")
    
    faissClient = FAISS()
    # faissClient.indexing(full_sentences)
    # faissClient.save_index("vectordb.index")
    faissClient.load_index("vectordb.index")
    query = "Meme Title: And Just Like That"
    
    query_embedding = np.array([get_embedding(query)]).astype("float32")

    k = 2
    distances, indices = faissClient.search(query_embedding, k)

    for i in range(k):
        print(f"Match {i+1}: {full_sentences[indices[0][i]]} (distance: {distances[0][i]:.4f})")