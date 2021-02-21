import requests
import csv
import os
from os.path import join, dirname
from dotenv import load_dotenv

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

TOKEN = os.environ.get("LingQ_API_KEY")
API_URL = 'https://www.lingq.com/api/v2/zh/cards/'
API_HEADER = {'Authorization':f'token {TOKEN}'}

r = requests.get(API_URL, headers=API_HEADER).json()
results = r["results"]

words = []

for result in results:
    word = result["hints"][0]
    words.append([word["id"],word["term"], " ".join(result["transliteration"]), word["text"], result["fragment"]]) # id, chinese, pinyin, japanese, phrase

with open('LingQ zh.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerows(words)