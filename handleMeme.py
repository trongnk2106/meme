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
                                    "For **each bounding box**, do the following:\n"
                                    "1. **Look closely** at the visual contents inside that box.\n"
                                    "2. Analyze the scene and context — what action, emotion, or idea is represented?\n"
                                    "3. Generate a **short, clever, and funny caption** for the content in that box.\n"
                                    "   - Use meme humor (relatable, absurd, ironic, satirical).\n"
                                    "   - Adapt tone based on image style (silly, sarcastic, dry, etc.).\n"
                                    "4. Ensure the caption fits **visually inside the box**:\n"
                                    "   - Add line breaks (`\\n`) manually where needed.\n"
                                    "   - Match the font size to the box size (small box = smaller font).\n"
                                    "   - Ensure text is readable — consider both **box background color** and surrounding image region.\n"
                                    "5. Choose a **text color** with **strong contrast** for legibility — use hex colors like `#FFFFFF`, `#000000`, `#FFD700`, etc.\n"
                                    "6. Output one JSON object per box, exactly in this format:\n\n"
                                    "[\n"
                                    "  {\n"
                                    "    \"id\": 1,\n"
                                    "    \"text\": \"Your hilarious caption here\\nWith line breaks if needed\",\n"
                                    "    \"fontSize\": 22,\n"
                                    "    \"color\": \"#FFFFFF\",\n"
                                    "    \"lineBreaks\": true\n"
                                    "  },\n"
                                    "  ...\n"
                                    "]\n\n"

                                    "Make sure the humor flows well across boxes, especially if they represent a conversation or sequence. Be bold, be clever, and make it MEME-WORTHY!"
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
    image_path = "D:/Pytorch-master/YokoMeme/images_full/Drake-Hotline-Bling.png"
    user_context="The \"Drake Hotline Bling\" meme template effectively communicates contrasting preferences or choices, showcasing a clear rejection followed by enthusiastic approval. In the first panel, Drake's disapproving gesture implies a strong dislike or refusal of an idea, concept, or action. Conversely, in the second panel, his expression transforms into one of excitement and endorsement, indicating a favorable view of an alternative option. This dynamic creates a humorous and relatable commentary on everyday decisions, societal norms, or opinions, allowing users to illustrate their approval or disapproval in a visually striking manner. The template's simplicity and engaging format make it highly adaptable, enabling users to convey complex attitudes with just a few words alongside the images."
    res = generator.generate_meme(image_path, user_context)
    breakpoint()
    draw_captions_on_image(image_path, res)
    # base_64_image = read_image(image_path)
    # width, height = get_width_height(image_path)
    # meme_topic = handle_requestCreateTopic(base_64_image, )
    # print(meme_topic)
    # breakpoint()
    # res = handle_requestOpenaiMEME(base_64_image, meme_topic, image_width=width, image_height=height)
    # breakpoint()
   
