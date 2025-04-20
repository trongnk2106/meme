from openai import OpenAI
import pandas as pd
import os
from dotenv import load_dotenv
import requests
from io import BytesIO
from PIL import Image
import base64

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)


def get_embedding(text, model="text-embedding-3-small"):
    response = client.embeddings.create(input=text, model=model)
    return response.data[0].embedding


import cv2
import numpy as np
from PIL import Image
import os


def draw_bbox(pil_image, box_infos, ImageWidth_infile, ImageHeight_infile):
    """
    Draw bounding boxes on a PIL image using OpenCV.

    Args:
        pil_image (PIL.Image): Image object from PIL.
        box_infos (list): List of box info dicts, each with x, y, width, height, rotateAngle.
        ImageWidth_infile (int): Width of original image for scale reference.
        ImageHeight_infile (int): Height of original image for scale reference.
        annot (list): List of annotation texts (e.g. labels or anything).
    """
    # Convert PIL image to OpenCV BGR format
    image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)

    image_width = image.shape[1]
    image_height = image.shape[0]

    ratio_width = image_width / ImageWidth_infile
    ratio_height = image_height / ImageHeight_infile

    for idx, box_info in enumerate(box_infos):
        x = int(box_info["x"] * ratio_width)
        y = int(box_info["y"] * ratio_height)
        w = int(box_info["width"] * ratio_width)
        h = int(box_info["height"] * ratio_height)
        angle = int(box_info["rotateAngle"])

        box_center = (x + w // 2, y + h // 2)
        box_size = (w, h)

        rotated_rect = (box_center, box_size, angle)
        box_points = cv2.boxPoints(rotated_rect).astype(np.int32)

        # Draw bounding box
        cv2.polylines(
            image, [box_points], isClosed=True, color=(3, 252, 61), thickness=2
        )

        # Draw ID text in the center-top of the box
        text = f"ID: {idx + 1}"
        text_position = (x + 10, box_center[1] - 10)
        cv2.putText(
            image, text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2
        )

    # Convert back to PIL if needed
    result_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    return result_image


def download_image(image_path):
    # download image by url
    response = requests.get(image_path)
    image = Image.open(BytesIO(response.content))
    return image


def image_to_base64(image: Image.Image, extension: str = "JPEG") -> str:
    buffered = BytesIO()
    image.save(buffered, format=extension.upper())  # hoặc PNG tùy ảnh
    return base64.b64encode(buffered.getvalue()).decode()


def get_description_for_image(csv_path, num_rows=10, get_all=False):
    df = pd.read_csv(csv_path)
    # select 10 first rows with loc
    if get_all:
        num_rows = df.shape[0]
    else:
        num_rows = num_rows if num_rows < df.shape[0] else df.shape[0]
    df = df.loc[:num_rows]
    df["sentence_full"] = (
        "Meme Title: " + df["meme_text"] + "\nImage Description: " + df["description"]
    )
    # sentence_full = "Meme Title: " + df['meme_text'] + "\nImage Description: " + df['description']
    return df
