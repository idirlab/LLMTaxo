import pandas as pd
import numpy as np
import json
import re
# import jsonlines
from tqdm import tqdm
# import nltk.data
from helpers import is_English, clean_text, split_sentences, apply_claimbuster
import csv
import time

# get claimbuster_score for each tweet
def get_tweets(infile, outfile):
    new_data = []
    with open(infile, 'r') as f:
        json_data = json.load(f)
        for tweet in tqdm(json_data, total=len(json_data)):
            elem = {}
            elem['tweet_id'] = tweet['tweet_id']
            elem['text'] = tweet['text']
            claim_score = apply_claimbuster(tweet['text'])
            elem['claim_score'] = claim_score
            # print(claim_score)
            new_data.append(elem)
    with open(outfile, 'w') as f:
        json.dump(new_data, f)

def get_tweets_from_json(infile, outfile):
    data = []
    cnt = 0
    with open(infile, 'r') as f:
        json_data = json.load(f)
        # json_data = json_data[:100]
        for tweet in tqdm(json_data, total=len(json_data)):
            if tweet['claim_score'] and tweet['claim_score']>0.5:      # claim_score > 0.5
                text = tweet['text']
                if is_English(text):                   # only keep english posts
                    text = " ".join(text.split())            # remove \n ...
                    data.append(text)
                cnt += 1

    with open(outfile, 'w') as f:
        for d in data:
            f.write(d + "\n")

# get facebook posts
def get_posts_from_csv(infile, outfile):
    df = pd.read_csv(infile)
    posts = df['Message'].values.tolist()
    # posts = posts[:100]
    final_posts = []
    cnt = 0
    for p in tqdm(posts, total=len(posts)):
        if is_English(p):                   # only keep english posts
            # p = clean_text(p)
            claim_score = apply_claimbuster(p)
            if claim_score and claim_score>0.5:   # claim_score > 0.5
                p = " ".join(p.split())            # remove \n ...
                final_posts.append(p)

    for p in final_posts[:5]:
        print(p)
        print()
    print(len(final_posts))

    # write .txt file
    with open(outfile, 'w') as f:
        for post in final_posts:
            f.write(post + "\n")

def posts_for_clustering(infile, outfile):
    with open(infile, 'r') as f:
        data = f.readlines()
    
    final_data = []
    for d in tqdm(data, total=len(data)):
        claim_score = apply_claimbuster(d)
        if claim_score and claim_score>0.5:
            final_data.append(d)
    print(len(final_data))

    with open(outfile, 'w') as f:
        for d in final_data:
            f.writelines(d + "\n")
    
def rm_line(infile, outfile):
    with open(infile, 'r') as f:
        data = f.readlines()
    
    with open(outfile, 'w') as f:
        for d in data:
            if d!="\n":
                f.writelines(d)

get_tweets("./dataset/covid19vax.json", "./dataset/covid19vax_CB.json")
get_tweets_from_json('../ClaimResolutionData/covid19vax_CB.json', './dataset/covid_posts_for_clustering.txt')
get_posts_from_csv('../ClaimResolutionData/crowdtangle/cybersecurity_010124-050724.csv', './dataset/cyber_posts_for_clustering.txt')
get_posts_from_csv("../ClaimResolutionData/crowdtangle/climate_010124-050724.csv", "./dataset/climate_posts_for_clustering.txt")
