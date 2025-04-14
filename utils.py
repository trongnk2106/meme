import openai
from openai import OpenAI
import pandas as pd
import os 
from dotenv import load_dotenv
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)
def get_embedding(text, model="text-embedding-3-small"):
    response = client.embeddings.create(
        input=text,
        model=model
    )
    return response.data[0].embedding


def get_description_for_image(csv_path, num_rows=10, get_all=False): 
    df = pd.read_csv(csv_path)
    # select 10 first rows with loc
    if get_all:
        num_rows = df.shape[0]
    else:
        num_rows = num_rows if num_rows < df.shape[0] else df.shape[0]
    df = df.loc[:num_rows]
    df['sentence_full'] = "Meme Title: " + df['meme_text'] + "\nImage Description: " + df['description']
    # sentence_full = "Meme Title: " + df['meme_text'] + "\nImage Description: " + df['description']
    return df


