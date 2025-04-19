

from src.pipeline.pipeline import MemePipeline
from src.pipeline.meme_generator import MemeGenerator

if __name__ == "__main__":
   
    user_input = "A person in trouble enquiring another person if it is their first time doing something "
    vector_db_name = "meme_collection"
    meme_generator = MemeGenerator()
    meme_pipeline = MemePipeline("http://103.186.100.39:6333", meme_generator, vector_db_name)
    results = meme_pipeline.pipeline(user_input, k=1)
    print(results)
    breakpoint()
    # for idx, result in enumerate(results):
       
