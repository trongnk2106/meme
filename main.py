

from src.pipeline.pipeline import MemePipeline
from src.pipeline.meme_generator import MemeGenerator
import os 
from dotenv import load_dotenv
load_dotenv()
db_url = os.getenv("QDRANT_URL")
if __name__ == "__main__":
    user_input = "A person in trouble enquiring another person if it is their first time doing something "
    vector_db_name = "meme_collection"
    meme_generator = MemeGenerator()
    meme_pipeline = MemePipeline(db_url, meme_generator, vector_db_name)
    meme_pipeline.pipeline(user_input, k=1)
 
       
