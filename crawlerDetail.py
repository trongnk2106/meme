# write crawler with request
import requests
import os
import re
import time
import random
# mutli-threading
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import json
id = 'rQ9HO_7EOz4toLAJGJhlG'
base_url = f"https://supermeme.ai/_next/data/{id}/en/meme/"




def handle_request(url) : 
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        # memes = data['memeTemplates']
        return data
    else:
        print("Failed to fetch data from the API")
        return None
    
if __name__ == "__main__": 
    result = []
    df = pd.read_csv("meme_data.csv")
    images_list = df['name']
    
    # url = base_url + images_list[0] +  ".json"
    # # multi-threading
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for quote in images_list:
            # random sleep time between 1 and 3 seconds
     
            url = base_url + quote +  ".json"
            
            future = executor.submit(handle_request, url)
            futures.append(future)
        
        for future in as_completed(futures):
            try:
                memes = future.result()
                if memes:
                    result.append(memes)
            except Exception as e:
                print(f"[!] Error getting future result: {e}")
    
    # dump to json
    with open("meme_data.json", "w") as f:
        json.dump(result, f, indent=4)
    print("Dumped to json")      
                
    
    