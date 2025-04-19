import json
import os

import base64
import os
import os
import re
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
import openai
from openai import OpenAI
import io
from src.utils.DrawMeme import draw_bbox_pillow
from src.utils.utils import (
    get_embedding,
    get_description_for_image,
    download_image,
    image_to_base64,
    draw_bbox,
)

load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=openai_key)


class MemeGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=openai_key)

    # def read_image(self, image_path):
    #     with open(image_path, "rb") as image_file:
    #         self.base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    # def get_width_height(self, image_path):
    #     with Image.open(image_path) as img:
    #         self.image_width, self.image_height = img.size

    def handle_requestCreateTopic(self, user_context, image_description):
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "You are a creative and funny meme generator AI.\n\n"
                                "Your task is to generate a **meme topic** that cleverly and humorously combines the user's intention with the visual content of an image.\n\n"
                                "### What you're given:\n"
                                "- An image that might contain a funny, ironic, awkward, or emotional moment.\n"
                                "- A user context — this is a phrase or sentence that hints at the intended mood, meaning, or joke setup.\n"
                                "- An optional **image description** extracted by a vision model, which helps you understand the scene, characters, and elements in the image.\n\n"
                                "### What you need to do:\n"
                                "- Analyze the image and the description.\n"
                                "- Understand the **tone and intent** of the user context.\n"
                                "- Then generate a **funny, clever, one-sentence meme topic** that captures the essence of both.\n"
                                "- Be witty, bold, and internet-meme-friendly — think like Reddit, Instagram, or Twitter meme humor.\n"
                                "- Keep it SHORT — just a meme topic, no explanation.\n\n"
                                "### FORMAT:\n"
                                "**Meme Topic:** <your single-sentence meme topic here>\n\n"
                                "---\n"
                                f'**User Context:** "{user_context}"\n'
                                f'**Image Description:** "{image_description}"\n'
                                "**Now generate a meme topic based on the image and context.**"
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{self.extension};base64,{self.base64_image}"
                            },
                        },
                    ],
                }
            ],
        )

        llm_response = response.choices[0].message.content

        if "**Topic:**" in llm_response:
            try:
                topic = llm_response.split("**Topic:**")[1].split("\n")[0].strip()
                self.meme_topic = topic
                # return topic
            except:
                self.meme_topic = llm_response
                # return llm_response
        else:
            self.meme_topic = llm_response
            # return llm_response

    def memegen(self):
        print("meme topic nef: ", self.meme_topic)
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": (
                                "You are a meme creator assistant with a sharp sense of humor and strong visual design skills.\n\n"
                                "=== CONTEXT ===\n"
                                f"{self.meme_topic}\n\n"
                                "=== INPUT ===\n"
                                "- An image containing several green bounding boxes.\n"
                                "- Each bounding box has a red ID number label.\n"
                                "- The IDs indicate the correct reading order for speech/text.\n\n"
                                "=== TASK ===\n"
                                "For each bounding box:\n"
                                "1. You MUST analyze the actual image below. Do NOT guess or imagine — look at the visual content in each bounding box, and write captions based on what you see. Treat this image as a real meme base (facial expressions, actions, context).\n"
                                "2. Write a short, clever, and funny caption (meme-style: ironic, absurd, relatable).\n"
                                "   - The caption must be a single line (no line breaks).\n"
                                "3. Choose a suitable **fontFamily** (e.g. 'Arial', 'Comic Sans MS', 'Impact') for each caption.\n"
                                "4. Determine whether the caption should be **bold** for visual emphasis.\n\n"
                                "=== TEXT COLOR ===\n"
                                "- Select **one single text color** (in hex, e.g. `#FFD700`, `#00FFFF`, `#FF69B4`, etc.) that works well across **all bounding boxes**.\n"
                                "- The color should be chosen based on the **combined average visual background of all bounding boxes**, ensuring strong contrast and good readability.\n"
                                "- Avoid choosing based only on a small part of a box or the full image background.\n"
                                "- Be expressive with the color choice — try something visually interesting and meme-friendly, not just black or white.\n"
                                "- Example tones: bright yellow for absurdity, pink for sass, mint for sarcasm, light blue for chill humor.\n\n"
                                "=== OUTPUT FORMAT ===\n"
                                "Return a list of caption objects. Each caption must include:\n"
                                "- id\n"
                                "- text\n"
                                "- fontFamily\n"
                                "- bold\n"
                                "- color (same color for all captions)\n\n"
                                "**Example format:**\n"
                                "[\n"
                                "  {\n"
                                '    "id": 1,\n'
                                '    "text": "Your hilarious caption here",\n'
                                '    "fontFamily": "Comic Sans MS",\n'
                                '    "bold": true,\n'
                                '    "color": "#FFD700"\n'
                                "  },\n"
                                "  ...\n"
                                "]\n\n"
                                "Only return the list of captions as shown. Make sure the color is the same in every caption object. Be bold, funny, and visually smart!"
                            ),
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/{self.extension};base64,{self.base64_image}"
                            },
                        },
                    ],
                }
            ],
            max_tokens=1400,
        )

        llm_reponse = response.choices[0].message.content
        breakpoint()
        json_str = re.search(r"```json\n(.*?)```", llm_reponse, re.DOTALL).group(1)
        res = json.loads(json_str)
        return res

    def generate_meme(self, image, user_context, image_description):
        # self.extension = os.path.splitext(image_url)[1][
        #     1:
        # ]  # Get the file extension without the dot
        # if self.extension.lower() not in ["jpg", "jpeg", "png"]:
        #     raise ValueError(
        #         "Unsupported image format. Please provide a JPG or PNG image."
        #     )
        # if self.extension.lower() == "jpg":
        #     self.extension = "jpeg"
        # print("Image URL: ", image_url)
        # image = download_image(image_url)
        # image_with_box = draw_bbox(image)
        # self.base64_image = image_to_base64(
        #     download_image(image_url), extension=self.extension
        # )
        self.handle_requestCreateTopic(user_context, image_description)
        res = self.memegen()
        return res


if __name__ == "__main__":

    generator = MemeGenerator()
    # Example image path
    root_path = "D:/Pytorch-master/YokoMeme/images_full"
    image_name = "20240812T111331432Z.jpeg"
    image_path = os.path.join(root_path, image_name)
    user_context = ""
    image_description = "The Adorable Chinese Gymnast Olympics Medal meme template communicates a sense of unbridled joy and triumph in the face of achievement. It embodies the excitement associated with winning or accomplishing a significant goal, likening personal victories to the euphoric moment of an athlete celebrating a gold medal. This template often juxtaposes the innocence and exuberance of success with everyday situations, making it relatable and motivational. It captures the essence of pride, whether in sports, personal endeavors, or any form of celebration, conveying a universally understood sentiment of happiness and fulfillment that resonates with audiences in various contexts."
    import time

    start = time.time()
    annot = generator.generate_meme(image_path, user_context, image_description)
    start_2 = time.time()
    print("Time taken for meme generation: ", start_2 - start)
    # annot = [{'id': 1, 'text': 'Me when \nthe boss \nsays they\'re \n"working from home"', 'fontSize': 20, 'color': '#FFFFFF', 'lineBreaks': True}]

    # breakpoint()
    # start_2 = time.time()
    print(annot)
    with open("filterJson.json", "r") as file:
        data = json.load(file)
    for item in data:
        if item["imageName"] == image_name:
            draw_bbox_pillow(
                item["imageName"],
                item["initialCaptions"],
                item["imageWidth"],
                item["imageHeight"],
                annot,
            )

    # end_2 = time.time()
    # end_3 = time.time()
    # print("Time taken for meme generation: ", end_2 - start)

    # breakpoint()
    # draw_captions_on_image(image_path, res)
    # base_64_image = read_image(image_path)
    # width, height = get_width_height(image_path)
    # meme_topic = handle_requestCreateTopic(base_64_image, )
    # print(meme_topic)
    # breakpoint()
    # res = handle_requestOpenaiMEME(base_64_image, meme_topic, image_width=width, image_height=height)
    # breakpoint()
