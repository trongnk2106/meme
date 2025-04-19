from qdrant_client import QdrantClient, models
from qdrant_client.models import PointStruct
from src.utils.utils import get_embedding, get_description_for_image
import numpy as np
import pandas as pd
class QdrantDBConnection:
    def __init__(self, url: str, collection_name: str = "meme_collection"):
        self.client = QdrantClient(url=url)
        self.collection_name = collection_name
   # Assuming 1536 is the size of your embeddings

    def __repr__(self):
        return f"QdrantDBConnection(url={self.client.url})"
    
    def get_info(self):
        info = self.client.get_info()
        print(f"QdrantDBConnection: {info}")

    def create_collection(self, collection_name: str, vector_size: int):
        self.client.create_collection(
                collection_name=f"{collection_name}",
                vectors_config=models.VectorParams(size=vector_size, distance=models.Distance.COSINE),
            )    
        
    def get_collection(self):
        collection = self.client.get_collection(collection_name = self.collection_name)
        print(f"Collection: {collection}")
        return collection
        
    def index_data(self, df, emb):
        if self.get_collection() is None:
            self.create_collection(self.collection_name, vector_size=len(emb[0]))
        self.points = [
        PointStruct(
            id=idx,
            vector=data,
            payload={"name": name, "text": text, "image_path": image_path},
        )
        for idx, (data, text, name, image_path) in enumerate(zip(emb, df['sentence_full'], df['name'], df['image_path']))
    ]
        self.client.upsert(self.collection_name, self.points)
        print(f"Indexed {len(self.points)} points to collection {self.collection_name}")
        
    def search(self, query_vector, limit=5):
        result = self.client.query_points(
            collection_name=self.collection_name,
            query=get_embedding(
                text=query_vector,
            ),
            limit=3,
        )     
        return result.points
        

# if __name__ == "__main__": 

#     df = get_description_for_image('./meme_data.csv', num_rows=10, get_all=False)
#     # list_of_embeddings = [get_embedding(text) for text in df['sentence_full']]
#     emb = np.load('embeddings.npy') 

    
#     qdrant_client = QdrantDBConnection(url="http://103.186.100.39:6333")
#     qdrant_client.index_data(df, emb)
    
#     res = qdrant_client.search("And Just Like That")

#     breakpoint()
#     print(res)    
#     # print(len(list_of_embeddings[0]))
    # list_of_embeddings = np.array(list_of_embeddings)
    # np.save('embeddings.npy', list_of_embeddings)
    
    # df = pd.read_csv("./meme_data.csv")
    # collection_name = "meme_collection"
    # client = QdrantClient(url="http://103.186.100.39:6333")
    # client.update_collection(
    #     collection_name=f"{collection_name}",
    #     optimizers_config=models.OptimizersConfigDiff(indexing_threshold=10000),
    # )
    # save to q