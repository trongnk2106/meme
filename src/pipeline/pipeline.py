import ast
import os
from src.database.connection import QdrantDBConnection
from src.pipeline.meme_generator import MemeGenerator
import numpy as np
import pandas as pd
from src.utils.utils import (
    get_embedding,
    get_description_for_image,
    download_image,
    image_to_base64,
    draw_bbox,
)

from PIL import Image, ImageDraw, ImageFont
from src.utils.DrawMeme import draw_bbox_pillow


class MemePipeline:
    def __init__(
        self, qdrant_url, meme_generator, vector_db_collection="meme_collection"
    ):
        self.qdrant_client = QdrantDBConnection(
            url=qdrant_url, collection_name=vector_db_collection
        )
        self.meme_generator = meme_generator

    def query_image_and_caption(self, query, k=1):
        results = self.qdrant_client.search(query, limit=k)
        list_of_memes = []
        list_images_urls = []
        list_image_names = []
        list_image_descriptions = []
        list_image_initial_captions = []
        list_image_widths = []
        list_image_heights = []

        # breakpoint()
        for result in results:
            meme_context = result.payload["text"]
            image_name = result.payload["name"]
            image_url = result.payload["image_url"]
            image_height = result.payload["image_height"]
            image_width = result.payload["image_width"]
            image_description = result.payload["image_description"]
            image_initial_captions = result.payload["initial_captions"]
            list_of_memes.append(meme_context)
            list_image_names.append(image_name)
            list_images_urls.append(image_url)
            list_image_descriptions.append(image_description)
            list_image_initial_captions.append(image_initial_captions)
            list_image_widths.append(image_width)
            list_image_heights.append(image_height)
        results_df = pd.DataFrame(
            {
                "meme_context": list_of_memes,
                "image_name": list_image_names,
                "image_url": list_images_urls,
                "image_description": list_image_descriptions,
                "image_initial_captions": list_image_initial_captions,
                "image_width": list_image_widths,
                "image_height": list_image_heights,
            }
        )

        return results_df

    def pipeline(self, query, k=1):
        list_meme = []
        df_info = self.query_image_and_caption(query, k=k)
        # print(df_info.head())
        for idx, row in df_info.iterrows():
            meme_context = row["meme_context"]
            image_url = row["image_url"]
            image_name = row["image_name"]
            image_height = row["image_height"]
            image_width = row["image_width"]
            image_description = row["image_description"]
            image_initial_captions = ast.literal_eval(row["image_initial_captions"])
            self.extension = os.path.splitext(image_url)[1][
                1:
            ]  # Get the file extension without the dot
            if self.extension.lower() not in ["jpg", "jpeg", "png"]:
                raise ValueError(
                    "Unsupported image format. Please provide a JPG or PNG image."
                )
            if self.extension.lower() == "jpg":
                self.extension = "jpeg"
            image = download_image(image_url)
            image_width_box = draw_bbox(
                image, image_initial_captions, image_width, image_height
            )

            image_width_box = image_to_base64(image_width_box, extension=self.extension)
            meme = self.meme_generator.generate_meme(
                image=image_width_box,
                user_context=query,
                image_description=image_description,
                extension=self.extension,
            )
            image_draw = draw_bbox_pillow(
                image=image,
                box_infos=image_initial_captions,
                ImageWidh_infile=image_width,
                ImageHeight_infile=image_height,
                annot=meme,
            )
            image_draw.show()
        # return image_draw
        # list_meme.append(meme)
        # for meme_context, image_url in zip(list_of_memes, list_images_urls):

        #     meme = self.meme_generator.generate_meme(
        #         image_url=image_url, user_context=query, image_description=meme_context
        #     )
        #     list_meme.append(meme)

        # return list_meme

    def draw_meme(self, image, meme_text, bbox=None):
        draw_bbox_pillow()
