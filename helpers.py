import requests
import json
# import jsonlines
from tqdm import tqdm
import re
# import nltk.data
from googletrans import Translator
from langdetect import detect
import time

translator = Translator()
requests.adapters.DEFAULT_RETRIES = 5
claimbuster_headers = {"x-api-key": 'claimbuster-api-key'}
# claimbuster_api = requests.session()
# claimbuster_api.keep_alive = False
def apply_claimbuster(input_claim):
    api_endpoint = f"https://idir.uta.edu/claimbuster//api/v2/score/text/{input_claim}"
    # response = claimbuster_api.get(url=api_endpoint, headers=claimbuster_headers)
    response = requests.get(url=api_endpoint, headers=claimbuster_headers)
    if response: 
        response = response.json()
    return response['results'][0]['score'] if response and response['results'] else None

# score = apply_claimbuster("I got vaccinated yesterdays")
# print("score: ", score)

def is_English(text):
    """
    check if tweet is English
    """
    # googletrans
    # try:
    #     dec_lan = translator.detect(text)
    #     if dec_lan.lang=='en': 
    #         return True
    #     else: return False
    # except Exception as e:
    #     print(f"Error found in googletrans: {e}")
    #     return False

    # langdetect
    try:
        dec_lan = detect(str(text))
        if dec_lan=='en': 
            return True
        else: return False
    except Exception as e:
        print(f"Error found in langdetect: {e}")
        # print(text)
        return False

A = "I got vaccinated yesterdays"
B = "Je me suis fait vacciner hier"
print(is_English(A))
print(is_English(B))

def clean_text(tweet):
    tweet = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', tweet)    # remove url
    tweet = re.sub("@[A-Za-z0-9_]+", '', tweet)               # remove @xxx
    tweet = tweet.replace("RT : ", "").replace("#", "")
    tweet = " ".join(tweet.split())            # remove \n ...
    return tweet