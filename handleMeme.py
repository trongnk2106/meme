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
from drawTextOnImage import draw_bbox_pillow
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=openai_key)



class MemeGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=openai_key)
        
    
    def read_image(self, image_path) : 
        with open(image_path, "rb") as image_file:
            self.base64_image = base64.b64encode(image_file.read()).decode("utf-8")

    
    def get_width_height(self, image_path):
        with Image.open(image_path) as img:
            self.image_width, self.image_height = img.size
        
    def handle_requestCreateTopic(self, user_context):
        response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        { 
                            "role": "user", 
                            "content": [
                                {
                                    "type": "text",
                                    "text": (
                                        "You are a meme generator AI. Given an image **and a user-provided context**, generate a meme topic "
                                        "that is funny, creative, and clearly inspired by both the image and the user's intention.\n\n"

                                        "### Input:\n"
                                        "- An image (e.g. showing funny or ironic situation)\n"
                                        "- A user context: a sentence or phrase provided by the user to guide the tone or topic of the meme.\n\n"

                                        "### Output:\n"
                                        "- A short meme topic (just a single sentence, no explanation).\n"
                                        "- It should combine visual content from the image and the vibe/hint from user context.\n\n"

                                        "### EXAMPLE:\n"
                                        "**Image:** (image of someone burning food in kitchen)\n"
                                        "**User Context:** 'I swear I followed the recipe!'\n"
                                        "**Expected Output:** 'cooking gone wrong'\n\n"

                                        "---\n"
                                        f"**User Context:** '{user_context}'\n"
                                        "**Now generate a meme topic for this image:**\n"
                                    )
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{self.base64_image}"
                                    }
                                }
                            ]
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
        

    
    def handle_requestOpenaiMEME(self):
        response = self.client.chat.completions.create(
                    model="gpt-4o",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                "text": (
                    "You are a world-class meme generator AI. Given an image and a topic, your task is to create TWO funny, clever, and highly contextual meme captions. "
                    "These captions should reflect what's visually happening in the image and be placed in a layout-aware way (e.g., top/bottom or left/right split).\n\n"

                    "### Image Layout:\n"
                    "- Most meme images are divided into two parts: either horizontally (top/bottom) or vertically (left/right).\n"
                    "- One caption should belong to each part, representing or reacting to what’s visually happening in that part.\n"

                    "### Your Job:\n"
                    "- Observe the image.\n"
                    "- Understand the topic and visual cues.\n"
                    "- Create two short, witty jokes or sarcastic comments (in English) that match each section of the image.\n"
                    "- Return a JSON object with full formatting and placement for each caption.\n"
                    "- All coordinates, sizes, and font values must be **scaled to the actual image size**: {image_width}x{image_height} pixels.\n"
                    "- Make sure the captions do not overlap or hide important content in the image.\n"
                    "- Font size should be proportional (e.g., around 3–5% of image height).\n\n"

                    "### Format:\n"
                    "{\n"
                    "  \"captions\": [\n"
                    "    {\n"
                    "      \"x\": int,        // pixel coordinate\n"
                    "      \"y\": int,\n"
                    "      \"text\": string,  // the actual joke caption\n"
                    "      \"width\": int,\n"
                    "      \"height\": int,\n"
                    "      \"fontSize\": int,\n"
                    "      \"language\": \"English\",\n"
                    "      \"fontFamily\": null,\n"
                    "      \"rotateAngle\": 0\n"
                    "    },\n"
                    "    {...}\n"
                    "  ]\n"
                    "}\n\n"

                    "### Example:\n"
                    "**Topic:** 'Cooking gone wrong'\n"
                    "**Image Size:** 512x512\n"
                    "**Output:**\n"
                    "{\n"
                    "  \"captions\": [\n"
                    "    {\n"
                    "      \"x\": 20,\n"
                    "      \"y\": 20,\n"
                    "      \"text\": \"Me trying to follow a recipe from TikTok\",\n"
                    "      \"width\": 470,\n"
                    "      \"height\": 60,\n"
                    "      \"fontSize\": 20,\n"
                    "      \"language\": \"English\",\n"
                    "      \"fontFamily\": null,\n"
                    "      \"rotateAngle\": 0\n"
                    "    },\n"
                    "    {\n"
                    "      \"x\": 20,\n"
                    "      \"y\": 440,\n"
                    "      \"text\": \"The smoke alarm judging every move\",\n"
                    "      \"width\": 470,\n"
                    "      \"height\": 60,\n"
                    "      \"fontSize\": 20,\n"
                    "      \"language\": \"English\",\n"
                    "      \"fontFamily\": null,\n"
                    "      \"rotateAngle\": 0\n"
                    "    }\n"
                    "  ]\n"
                    "}\n\n"

                    "---\n"
                    f"Now generate meme captions for the following:\n"
                    f"- Topic: '{self.meme_topic}'\n"
                    f"- Image size: {self.image_width} x {self.image_height} pixels\n"
                )
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{self.base64_image}"
                                    }
                                }
                            ]
                        }
                    ],
                    max_tokens=1000,
                )

        llm_reponse = response.choices[0].message.content

        json_str = re.search(r'```json\n(.*?)```', llm_reponse, re.DOTALL).group(1)
        res = json.loads(json_str)

        return res
    def memegen(self):
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
                        "1. Analyze the visual content inside the box (facial expressions, actions, context).\n"
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
                        "    \"id\": 1,\n"
                        "    \"text\": \"Your hilarious caption here\",\n"
                        "    \"fontFamily\": \"Comic Sans MS\",\n"
                        "    \"bold\": true,\n"
                        "    \"color\": \"#FFD700\"\n"
                        "  },\n"
                        "  ...\n"
                        "]\n\n"

                        "Only return the list of captions as shown. Make sure the color is the same in every caption object. Be bold, funny, and visually smart!"
                    )
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{self.base64_image}"
                    }
                }
            ]
        }
    ],
    max_tokens=1400,
)

        llm_reponse = response.choices[0].message.content

        json_str = re.search(r'```json\n(.*?)```', llm_reponse, re.DOTALL).group(1)
        res = json.loads(json_str)

        return res

    def generate_meme(self, image_path, user_context):
        self.read_image(image_path)
        self.get_width_height(image_path)
        self.handle_requestCreateTopic(user_context)
        res = self.memegen()
        return res




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

    generator = MemeGenerator()
    # Example image path
    root_path = "D:/Pytorch-master/YokoMeme/images_full"
    image_name = "Im-going-to-change-the-world-For-the-better-right-Star-Wars.png"
    image_path = os.path.join(root_path, image_name)
    user_context= "The \"I'm going to change the world. For the better, right?\" meme template effectively communicates the duality of hope and skepticism regarding ambitious intentions. It captures the essence of idealism when someone expresses a noble desire to improve the world, yet pairs that optimism with a question that introduces doubt, highlighting the complexity of enacting real change. This juxtaposition resonates widely, reflecting a shared experience of facing harsh realities while aspiring to achieve positive outcomes. By incorporating elements of irony, the template invites reflection on the challenges and uncertainties that often accompany efforts to create a better future, making it relevant to a broad spectrum of social and political discourse."
    annot = generator.generate_meme(image_path, user_context)
    
    # annot = [{'id': 1, 'text': 'Me when \nthe boss \nsays they\'re \n"working from home"', 'fontSize': 20, 'color': '#FFFFFF', 'lineBreaks': True}]

    # breakpoint()
    print(annot)
    with open("filterJson.json", 'r') as file:
        data = json.load(file)
    for item in data:
        if item["imageName"] == image_name:
            draw_bbox_pillow(item["imageName"], item["initialCaptions"], item["imageWidth"], item['imageHeight'], annot)
        
    
    
    # breakpoint()
    # draw_captions_on_image(image_path, res)
    # base_64_image = read_image(image_path)
    # width, height = get_width_height(image_path)
    # meme_topic = handle_requestCreateTopic(base_64_image, )
    # print(meme_topic)
    # breakpoint()
    # res = handle_requestOpenaiMEME(base_64_image, meme_topic, image_width=width, image_height=height)
    # breakpoint()
   
