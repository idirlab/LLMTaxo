import json
import pandas as pd
from collections import defaultdict

def get_statistics(infile):
    with open(infile, 'r') as f:
        statistics = defaultdict(int)
        data = json.load(f)
        data = data['clusters']
        print(len(data))
        for d in data:
            statistics[int(d["cluster_size"])] += 1
        sorted_s = sorted(statistics.items(), key=lambda x: x[0])
        print(sorted_s)

def get_posts(infile, outfile):
    tweets = []
    with open(infile, 'r') as f:
        data = json.load(f)
        data = data['clusters']
        i = 1
        seen = set()
        for d in data:
            if int(d["cluster_id"]) != -1:
                tweet_text = d["cluster"][0]["tweet_text"]
                if tweet_text and tweet_text not in seen:
                    tweets.append([i, d["cluster"][0]["tweet_text"]])
                    seen.add(tweet_text)
                    i += 1
    print(len(tweets))

    # write to excel
    df = pd.DataFrame(tweets)
    # insert header
    df.columns = ["#", "tweet"]
    df.to_excel(outfile, index=False, header=True)

def random_pick(infile, outfile):
    # random select 100 lines from excel sheet
    df = pd.read_excel(infile)
    df_ran = df.sample(100)
    print(df_ran)
    df_ran.to_excel(outfile, index=False, header=True)

if __name__ == "__main__":
    # get_statistics("./dataset/cyber_results_HDBSCAN.json")
    get_posts("./dataset/covid_clustering_results.json", "./dataset/covid_posts_togen.xlsx")
    get_posts("./dataset/cyber_clustering_results.json", "./dataset/cyber_posts_togen.xlsx")
    get_posts("./dataset/climate_clustering_results.json", "./dataset/climate_posts_togen.xlsx")

    # select 100 posts for topic annotation
    # random_pick("./dataset/covid_posts_togen.xlsx", "./dataset/covid_posts_100.xlsx")
    # random_pick("./dataset/cyber_posts_togen.xlsx", "./dataset/cyber_posts_100.xlsx")
    # random_pick("./dataset/climate_posts_togen.xlsx", "./dataset/climate_posts_100.xlsx")