import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.cluster import HDBSCAN
# from hdbscan import HDBSCAN
from sklearn import metrics
import re
import collections
import json
from tqdm import tqdm
from data_preprocess.helpers import clean_text, split_sentences, apply_claimbuster, is_English
import time
from sklearn.metrics import silhouette_samples, silhouette_score


np.random.seed(1)


def get_data(filename):     # list
    with open(filename, 'r') as f:
        data = f.readlines()
        return data

def get_csv_data(filename):
    data = []
    df = pd.read_csv(filename)
    for row in tqdm(df.values.tolist(), total=len(df)):
        tweet = row[0]
        # id_list = row[1]
        data.append(tweet)
    print(len(data))
    return data

def json_to_list(filename):
    data = []
    with open(filename, 'r') as f:
        json_data = json.load(f)
        for i, c in enumerate(json_data['clusters']):
            if "cluster-1" in c:
                for tweet in c['cluster-1']:
                    data.append(tweet['tweet_text'])
            elif "cluster2" in c:
                for tweet in c['cluster2']:
                    data.append(tweet['tweet_text'])
    return data

def get_clean_tweets(infile):
    data = []
    cnt = 0
    with open(infile, 'r') as f:
        json_data = json.load(f)
        for tweet in tqdm(json_data, total=len(json_data)):
            if cnt%500 == 0: 
                time.sleep(5)
            if tweet['claim_score'] and tweet['claim_score']>0.5:
                text = clean_text(tweet['text'])
                if is_English(text):
                    data.append(text)
                cnt += 1
    return data

def clustering(data, outfile, min_size):
    # sentence bert
    embedder = SentenceTransformer('paraphrase-distilroberta-base-v1')
    # data = data[:1000]   # for testing
    corpus_embeddings = embedder.encode(data, show_progress_bar=True)
    # Normalize the embeddings to unit length
    corpus_embeddings = corpus_embeddings /  np.linalg.norm(corpus_embeddings, axis=1, keepdims=True)
    # print(corpus_embeddings.size)
    # print(corpus_embeddings[1][0])
    # print(corpus_embeddings.shape)

    print("Clustering...")
    
    # HDBSCAN
    clustering_model = HDBSCAN(min_cluster_size = min_size, metric='euclidean', max_cluster_size=3000)  # , cluster_selection_epsilon=0.827   
    cluster_assignment = clustering_model.fit_predict(corpus_embeddings)
    print("Clustering done")
    print(cluster_assignment)
    print("start to evaluate clusters...")
    # evaluate with silhouette score while exlude cluster -1
    non_noise_mask = cluster_assignment != -1
    non_noise_cluster_assignment = cluster_assignment[non_noise_mask]
    non_noise_corpus_embeddings = corpus_embeddings[non_noise_mask]
    silh_score = silhouette_score(corpus_embeddings, cluster_assignment, metric='euclidean')
    silh_score_non_noise = silhouette_score(non_noise_corpus_embeddings, non_noise_cluster_assignment, metric='euclidean')
    print("Silhouette score: ", silh_score)
    print("Silhouette score non noise: ", silh_score_non_noise)


    clustered_sentences = {}
    for sentence_id, cluster_id in enumerate(cluster_assignment):
        if cluster_id not in clustered_sentences:
            clustered_sentences[cluster_id] = []
        clustered_sentences[cluster_id].append(tweets_list[sentence_id])


    # write to json
    json_data = {"clusters": []}
    for i, cluster in clustered_sentences.items():
        # if i!=-1 and i!=0:
        tweet_cluster = []
        for c in cluster:
            tweet_cluster.append({
                "tweet_text": c,
            })
            
        json_data["clusters"].append({
            "cluster_id": str(i),
            "cluster_size": str(len(cluster)),
            "isClaim": "T",
            "claim": "",
            "cluster": tweet_cluster})

    with open(outfile, 'w') as f:
        json.dump(json_data, f)

    print("# of entries: " + str(len(tweets_list)))
    print("# of clusters: " + str(len(clustered_sentences)))



if __name__ == "__main__":
    # tweets_list = get_clean_tweets('../ClaimResolutionData/covid19vax_CB.json')


    # read from .txt
    # tweets_list = get_data('../ClaimResolutionData/covid_posts_for_clustering.txt')
    # tweets_list = get_data('../ClaimResolutionData/cyber_posts_for_clustering.txt')
    tweets_list = get_data('../ClaimResolutionData/climate_posts_for_clustering.txt')

    # tweets_list = tweets_list[:1000]
    # for i in range(10):
    #     print(tweets_list[i])
    #     print("\n")
    # print(len(tweets_list))
    # clustering(tweets_list, '../ClaimResolutionData/covid_clustering_results.json', 3)
    # clustering(tweets_list, '../ClaimResolutionData/cyber_clustering_results.json', 2)
    clustering(tweets_list, '../ClaimResolutionData/climate_clustering_results.json', 2)

