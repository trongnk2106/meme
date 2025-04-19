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


base_url = "https://supermeme.ai/api/search?searchQuery="
adult_memes = ["the rock"]


def handle_request(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        memes = data["memeTemplates"]
        return memes
    else:
        print("Failed to fetch data from the API")
        return None


if __name__ == "__main__":
    result = []
    # multi-threading
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = []
        for quote in adult_memes:
            # random sleep time between 1 and 3 seconds

            url = base_url + quote

            future = executor.submit(handle_request, url)
            futures.append(future)

        for future in as_completed(futures):
            try:
                memes = future.result()
                if memes:
                    result.extend(memes)
            except Exception as e:
                print(f"[!] Error getting future result: {e}")

    # save to csv
    df = pd.DataFrame(result)
    df.to_csv("meme_data_4.csv", index=False)
