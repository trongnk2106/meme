import json
from qdrant_client import QdrantClient, models
from qdrant_client.models import PointStruct
import sys

# sys.path.append("..")
from src.utils.utils import get_embedding, get_description_for_image
import numpy as np
import pandas as pd


class QdrantDBConnection:
    def __init__(self, url: str, collection_name: str = "meme_collection_100"):
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
            vectors_config=models.VectorParams(
                size=vector_size, distance=models.Distance.COSINE
            ),
        )

    def collection_exists(self, collection_name):
        collections_response = self.client.get_collections()
        collection_names = [c.name for c in collections_response.collections]
        return collection_name in collection_names

    def index_data(self, df, emb):

        if not self.collection_exists(self.collection_name):
            self.create_collection(self.collection_name, vector_size=len(emb[0]))
        self.points = [
            PointStruct(
                id=idx,
                vector=data,
                payload={
                    "name": name,
                    "text": text,
                    "image_url": image_path,
                    "image_description": df["imageDescription"][idx],
                    "image_width": df["imageWidth"][idx],
                    "image_height": df["imageHeight"][idx],
                    "initial_captions": df["initialCaptions"][idx],
                },
            )
            for idx, (data, text, name, image_path) in enumerate(
                zip(emb, df["sentence_full"], df["name"], df["image_path"])
            )
        ]
        self.client.upsert(self.collection_name, self.points)
        print(f"Indexed {len(self.points)} points to collection {self.collection_name}")

    def search(self, query_vector, limit=5):
        result = self.client.query_points(
            collection_name=self.collection_name,
            query=get_embedding(
                text=query_vector,
            ),
            limit=limit,
        )
        return result.points


# if __name__ == "__main__":

#     df = get_description_for_image('../assets/meme_data_full.csv', num_rows=100, get_all=False)
#     # list_of_embeddings = [get_embedding(text) for text in df['sentence_full']]
#     # save the embeddings to a file
#     # np.save('embeddings.npy', list_of_embeddings)
#     emb = np.load('embeddings.npy')

#     # with open("../assets/filterJson.json" , "r") as f:
#     #     json_data = json.load(f)

#     # for item in json_data:

#     #     imageName = item['imageName']
#     #     imageDescription = item['imageDescription']
#     #     imageWidth = item['imageWidth']
#     #     imageHeight = item['imageHeight']
#     #     initialCaptions = item['initialCaptions']
#     #     if imageName not in df['name'].values:
#     #         print(f"Image {imageName} not found in DataFrame")
#     #         continue
#     #     idx = df[df['name'] == imageName].index[0]
#     #     df.at[idx, 'imageDescription'] = imageDescription
#     #     df.at[idx, 'imageWidth'] = imageWidth
#     #     df.at[idx, 'imageHeight'] = imageHeight
#     #     df.at[idx, 'initialCaptions'] = initialCaptions

#         # df[df['name'] == imageName]['imageDescription'] = imageDescription
#         # df[df['name'] == imageName]['imageWidth'] = imageWidth
#         # df[df['name'] == imageName]['imageHeight'] = imageHeight
#         # df[df['name'] == imageName]['initialCaptions'] = initialCaptions


#     # df.to_csv("../assets/meme_data_full.csv", index=False)


#     # breakpoint()

#     qdrant_client = QdrantDBConnection(url="http://103.186.100.39:6333")
#     qdrant_client.index_data(df, emb)

#     # res = qdrant_client.search("And Just Like That")

#     breakpoint()
# print(res)
# print(len(list_of_embeddings[0]))
# list_of_embeddings = np.array(list_of_embeddings)
# np.save('embeddings.npy', list_of_embeddings)

# df = pd.read_csv("./meme_data.csv")
# collection_name = "meme_collection"
# client = QdrantClient(url="http://103.186.100.39:6333")
# client.update_collection(
#     collection_name=f"{collection_name}",
#     optimizers_config=models.OptimizersConfigDiff(indexing_threshold=10000),
# )
