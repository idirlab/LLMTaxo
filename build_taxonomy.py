import csv
import pandas as pd
from collections import Counter, defaultdict

# read csv file
def read_results(infile, broad_file, medium_file, detailed_file):
    with open(infile, 'r') as file:
        broad_topics, medium_topics, detailed_topics, very_detailed_topics = [], [], [], []
        reader = csv.reader(file)
        next(reader, None)
        for row in reader:
            broad_topics.append(row[2])
            if len(row) > 3:
                medium_topics.append(row[3]) 
            if len(row) > 4:
                detailed_topics.append(row[4])
            if len(row) > 5:
                very_detailed_topics.append(row[5])
    
    broad_cnt = Counter(broad_topics)
    medium_cnt = Counter(medium_topics)
    detailed_cnt = Counter(detailed_topics)
    very_detailed_cnt = Counter(very_detailed_topics)


    # print("Broad topics: ", broad_cnt)
    # write to csv file and sort by value
    with open(broad_file, 'w') as file:
        writer = csv.writer(file)
        for key, value in broad_cnt.most_common():
            writer.writerow([key, value])

    # print("Medium topics: ", medium_cnt)
    # write to csv file and sort by value
    with open(medium_file, 'w') as file:
        writer = csv.writer(file)
        for key, value in medium_cnt.most_common():
            writer.writerow([key, value])

    with open(detailed_file, 'w') as file:
        writer = csv.writer(file)
        for key, value in detailed_cnt.most_common():
            writer.writerow([key, value])

def merge_topics_to_other(infile, outfile):
    with open(infile, 'r') as file:
        # merge broad
        broad_other = []
        broad_topics = []
        reader = csv.reader(file)
        data = list(reader)[1:]
        new_data = data
        for row in data:
            broad_topics.append(row[2])
        
        broad_cnt = Counter(broad_topics)
        for k, v in broad_cnt.items():
            if v < 50:
                broad_other.append(k)

        for i, b in enumerate(broad_topics):
            if b in broad_other:
                new_data[i][2] = "Other"

        # merge medium
        data = new_data
        T = defaultdict(list)
        for i, row in enumerate(data):
            medium = row[3] if len(row)>3 else None
            T[row[2]].append(medium)

        seen = []
        for k, v in T.items():
            for kk, vv in Counter(v).items():
                if vv > 4:
                    seen.append((k, kk))

        for i, row in enumerate(data):
            if len(row)>3 and (row[2], row[3]) not in seen:
                new_data[i][3] = "Other"
    
        # merge detailed
        data = new_data
        T = defaultdict(list)
        for i, row in enumerate(data):
            if len(row)>3:
                detailed = row[4] if len(row)>4 else None
                T[row[3]].append(detailed)

        seen = []
        for k, v in T.items():
            for kk, vv in Counter(v).items():
                if vv > 3:
                    seen.append((k, kk))
        
        for i, row in enumerate(data):
            if len(row)>4 and (row[3], row[4]) not in seen:
                new_data[i][4] = "Other"

        for i, row in enumerate(new_data):
            if len(row)>4 and "Broad topic: " in new_data[i][4]:
                new_data[i][4] = new_data[i][4].replace("Broad topic: ", "")
                new_data[i][4] = new_data[i][4].split("\n")[0]
            if len(row)>4 and "Medium topic: " in new_data[i][4]:
                new_data[i][4] = new_data[i][4].replace("Medium topic: ", "")
                new_data[i][4] = new_data[i][4].split("\n")[0]
            if len(row)>4 and row[3] == "Other":
                new_data[i][4] = None

        # write to csv
        with open(outfile, 'w', newline='') as f:
            csvwriter = csv.writer(f, delimiter = ',', lineterminator='\r\n', quotechar='"', escapechar='"')
            csvwriter.writerow(["#", "tweet", "broad_topic", "medium_topic", "detailed_topic"])
            for row in new_data:
                csvwriter.writerow(row)


def taxonomy(infile, outfile):
    G = defaultdict(lambda: defaultdict(lambda: set()))

    # read csv file
    with open(infile, 'r') as f:
        reader = csv.reader(f)
        infer_results = list(reader)[1:]
        for row in infer_results:
            # get each columns
            claim = row[1]
            broad_topic = row[2]
            medium_topic = row[3] if len(row)>3 else None
            detailed_topic = row[4] if len(row)>4 else None
            G[broad_topic][medium_topic].add(detailed_topic)

    new_data = []
    for k, v in G.items():
        for kk, vv in v.items():
            for vvv in vv:
                new_data.append([k, kk, vvv])

    # write to csv
    with open(outfile, 'w', newline='') as f:
        csvwriter = csv.writer(f, delimiter = ',', lineterminator='\r\n', quotechar='"', escapechar='"')
        csvwriter.writerow(["broad_topic", "medium_topic", "detailed_topic"])
        for row in new_data:
            csvwriter.writerow(row)

def get_statistics(infile, category):
    if category == "broad":
        x, y = 2, 3
    elif category == "medium":
        x, y = 3, 4
    elif category == "detailed":
        with open(infile, 'r') as f:
            detailed_topics = []
            reader = csv.reader(f)
            data = list(reader)[1:]
            for row in data:
                if len(row)>4:
                    detailed_topics.append(row[4])
        print(len(set(detailed_topics)))
        # print(set(detailed_topics))
        return     

    # read csv file
    with open(infile, 'r') as f:
        reader = csv.reader(f)
        data = list(reader)[1:]
        T = defaultdict(list)
        for i, row in enumerate(data):
            if len(row)>x:
                medium = row[y] if len(row)>y else None
                T[row[x]].append(medium)
    print(len(T))
    # for k, v in T.items():
    #     print(k)
    #     for kk, vv in Counter(v).items():
    #         print(kk, vv)
    #     print("----")

def taxonomy_analysis(infile):
    df = pd.read_csv(infile)
    broad_cnt = Counter(df['broad_topic'])
    medium_cnt = Counter(df['medium_topic'])
    detailed_cnt = Counter(df['detailed_topic'])

    # print(len(broad_cnt))
    # print(len(medium_cnt))
    # print(len(detailed_cnt))

    print("Broad topics: ")
    for k, v in broad_cnt.most_common():
        print(k, v)
    print("----------------")
    print("Medium topics: ")
    for k, v in medium_cnt.most_common():
        print(k, v)
    print("----------------")
    print("Detailed topics: ")
    for k, v in detailed_cnt.most_common():
        print(k, v)

def ori_data_analysis():
    df = pd.read_excel('./dataset/climate_posts_100.xlsx')
    df.head()

    broad_topics, medium_topics, detailed_topics, very_detailed_topics = [], [], [], []
    for idx, row in df.iterrows():
        if idx == 90:
            break
        broad_topic = "" if pd.isna(row['Broad Topic']) else row['Broad Topic'] 
        medium_topic = "" if pd.isna(row['Medium Topic']) else row['Medium Topic']
        detailed_topic = "" if pd.isna(row['Detailed Topic']) else row['Detailed Topic']
        # very_detailed_topic = "" if pd.isna(row['Very Detailed Topic']) else row['Very Detailed Topic']
        broad_topics.append(broad_topic)
        medium_topics.append(medium_topic)
        detailed_topics.append(detailed_topic)
        # very_detailed_topics.append(very_detailed_topic)

    broad_cnt = Counter(broad_topics)
    medium_cnt = Counter(medium_topics)
    detailed_cnt = Counter(detailed_topics)
    # very_detailed_cnt = Counter(very_detailed_topics)

    print("Broad topics: ")
    # print in descending order
    for k, v in broad_cnt.most_common():
        print(k, v)
    print("-------")
    print("Medium topics: ")
    for k, v in medium_cnt.most_common():
        print(k, v)


if __name__ == "__main__":
    # read_results('./dataset/climate_infer_results_gpt.csv', './dataset/climate_gpt_broad_topics.csv', 
    # './dataset/climate_gpt_medium_topics.csv', './dataset/climate_gpt_detailed_topics.csv')

    # ori_data_analysis()

    # build taxonomy
    merge_topics_to_other('./dataset/climate_infer_results_gpt.csv', './dataset/climate_results_merged_topics_gpt.csv')
    taxonomy('./dataset/climate_results_merged_topics_gpt.csv', './dataset/climate_taxonomy_gpt.csv')
    # get_statistics('./dataset/climate_results_merged_topics_gpt.csv', "broad")
    # get_statistics('./dataset/climate_results_merged_topics_gpt.csv', "medium")
    # get_statistics('./dataset/climate_results_merged_topics_gpt.csv', "detailed")