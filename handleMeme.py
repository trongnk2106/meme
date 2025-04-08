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
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_key)
def read_image(image_path) : 
    with open(image_path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode("utf-8")
    return encoded_string

def get_width_height(image_path):
    with Image.open(image_path) as img:
        width, height = img.size
    return width, height

def handle_requestCreateTopic(base64_image, user_context):
    response = client.chat.completions.create(
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
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ],
)
    breakpoint()
    llm_response = response.choices[0].message.content

    if "**Topic:**" in llm_response:
        try:
            topic = llm_response.split("**Topic:**")[1].split("\n")[0].strip()
            return topic
        except:
            return llm_response
    else:
        return llm_response
def handle_requestOpenaiMEME(base64_image, meme_topic, image_width, image_height):
    response = client.chat.completions.create(
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
    f"- Topic: '{meme_topic}'\n"
    f"- Image size: {image_width} x {image_height} pixels\n"
)
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/jpeg;base64,{base64_image}"
                    }
                }
            ]
        }
    ],
    max_tokens=1000,
)
    breakpoint()
    llm_reponse = response.choices[0].message.content

    json_str = re.search(r'```json\n(.*?)```', llm_reponse, re.DOTALL).group(1)
    res = json.loads(json_str)

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
    image_path = "D:\Pytorch-master\YokoMeme\images\Whisper-and-Goosebumps.png"
    base_64_image = read_image(image_path)
    width, height = get_width_height(image_path)
    meme_topic = handle_requestCreateTopic(base_64_image, user_context="A person saying something that generates goosebumps")
    print(meme_topic)
    breakpoint()
    res = handle_requestOpenaiMEME(base_64_image, meme_topic, image_width=width, image_height=height)
    breakpoint()
    draw_captions_on_image(image_path, res)
