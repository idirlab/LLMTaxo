from google import genai
import pandas as pd
import csv
import time


def get_prompt_examples():
    # df = pd.read_excel('./dataset/covid19vax_tweets.xlsx')
    # df = pd.read_excel('./dataset/cyber_posts_100.xlsx')
    df = pd.read_excel('./dataset/climate_posts_100.xlsx')
    df.head()

    prompt_examples = []
    n = len(df)
    for idx, row in df.iterrows():
        tweet = row['tweet']
        num = row['#']
        broad_topic = "" if pd.isna(row['Broad Topic']) else "Broad topic: " + row['Broad Topic'] 
        medium_topic = "" if pd.isna(row['Medium Topic']) else "; Medium topic: " + row['Medium Topic']
        detailed_topic = "" if pd.isna(row['Detailed Topic']) else "; Detailed topic: " + row['Detailed Topic']    




        # prompt covid tweets index: [2, 59, 7, 10, 22, 53, 20, 60, 33, 74, 81, 83]
#         user = {
#             "role": "user",
#             "content": "You will be given a tweet related to Covid-19 vaccine. Please generate topics for the tweet from different granularities such as broad topic, \
# medium topic, and detailed topic, separated by semicolon. Each generated topic should be no more than eight words and you should try to minimize the number of topics generated. \
# Here is a list of existing topics:\
# 1. Broad topic: Government Policies; Medium topic: Vaccine Mandates; Detailed topic: Opposition to Vaccine Mandates; \
# 2. Broad topic: Government Policies; Medium topic: Vaccine Policies; Detailed topic: Vaccine Privacy; \
# 3. Broad topic: Vaccine Safety and Effectiveness; Medium topic: Vaccine Side Effects; Detailed topic: Vaccine-Related Injuries and Deaths; \
# 4. Broad topic: Vaccine Safety and Effectiveness; Medium topic: Vaccine Side Effects; Detailed topic: Myocarditis Side Effect; \
# 5. Broad topic: Vaccine Safety and Effectiveness; Medium topic: Vaccine Side Effects; Detailed topic: Cancer Side Effect; \
# 6. Broad topic: Vaccine Safety and Effectiveness; Medium topic: Scientific and Medical Discussions; Detailed topic: Discussions about Hepatitis; \
# 7. Broad topic: Political and Societal Implications; Medium topic: Conspiracy Theories; \
# 8. Broad topic: Political and Societal Implications; Medium topic: Vaccine Injury; \
# 9. Broad topic: Personal Experiences and Opinions; Medium topic: Vaccine Refusal; \
# 10. Broad topic: Public Opinion; Medium topic: Vaccine Acceptance; \
# 11. Broad topic: Vaccine Distribution and Administration; Medium topic: Vaccine Impact; Detailed topic: Vaccine Impact on Heart Disease; \
# 12. Broad topic: Vaccine Production; Medium topic: Vaccine Manufacturing; Detailed topic: Investigation of  Manufacturers; \
# Please try to generate topics for the tweet using existing topics. If there is no good match, then generate new topics. \
# Here is the post: " + tweet,
#         }





        # prompt cybersecurity posts: 
#         user = {
#             "role": "user",
#             "content": "You will be given a Facebook post related to cybersecurity. Please generate topics for the post from different granularities such as broad topic, \
# medium topic, and detailed topic, separated by semicolon. Each generated topic should be no more than eight words and you should try to minimize the number of topics generated. \
# Here is a list of existing topics:\
# 1. Broad topic: Threats; Medium topic: Cyberattacks; Detailed topic: Chinese Cyberattacks on Philippine Websites; \
# 2. Broad topic: Threats; Medium topic: Phishing Attacks; Detailed topic: Phishing Examples; \
# 3. Broad topic: Threats; Medium topic: Data Breaches; Detailed topic: Home Depot Data Breach; \
# 4. Broad topic: Corporate Security; Medium topic: Recycling and Disposal Policies; Detailed topic: IT Equipment Disposal; \
# 5. Broad topic: Corporate Security; Medium topic: Small Business Cybersecurity; \
# 6. Broad topic: Policies and Governance; Medium topic: International Cooperation; Detailed topic: Cybersecurity Partnership Between Slovenia and U.S.; \
# 7. Broad topic: Policies and Governance; Medium topic: Government Regulations; Detailed topic: Challenges in Cybersecurity Information Sharing; \
# 8. Broad topic: Emerging Trends; Medium topic: Cloud Security; Detailed topic: Cloud Repatriation; \
# 9. Broad topic: Emerging Trends; Medium topic: Cybersecurity Events; \
# 10. Broad topic: Security Solutions; Medium topic: Data Protection; Detailed topic: Encrypted USB; \
# 11. Broad topic: Incident Management; Medium topic: Digital Forensics; Detailed topic: Insights into Digital Forensics; \
# 12. Broad topic: Workforce; Medium topic: Leadership; Detailed topic: Leadership Gaps; \
# 13. Broad topic: Education; Medium topic: Cybersecurity Training; Detailed topic: Vulnerability Assessment and Penetration Testing Training; \
# Please try to generate topics for the post using existing topics. If there is no good match, then generate new topics. \
# Here is the post: " + tweet,
#         }


# Here is a list of existing topics:\
# 1. Broad topic: Policies and Governance; Medium topic: International Climate Cooperation; Detailed topic: Global Food Security; \
# 2. Broad topic: Policies and Governance; Medium topic: Government Climate Action; Detailed topic: Infrastructure and Climate Mitigation; \
# 3. Broad topic: Economic and Social Impacts; Medium topic: Agriculture; Detailed topic: Food Security; \
# 4. Broad topic: Economic and Social Impacts; Medium topic: Public Health; Detailed topic: Deaths Due to Heatwaves; \
# 5. Broad topic: Activism and Public Awareness; Medium topic: Climate Advocacy; Detailed topic: Impact on Children; \
# 6. Broad topic: Activism and Public Awareness; Medium topic: Protests; Detailed topic: Climate Protests in National Archives; \
# 7. Broad topic: Environmental Impact; Medium topic: Biodiversity; Detailed topic: Marine Biodiversity; \
# 8. Broad topic: Environmental Impact; Medium topic: Global Warming; Detailed topic: Record-breaking Temperatures; \
# 9. Broad topic: Mitigation Solutions; Medium topic: Ecosystem Restoration; Detailed topic: Coastal Ecosystem Restoration; \
# 10. Broad topic: Mitigation Solutions; Medium topic: Renewable Energy; Detailed topic: Biodiesel; \
# 11. Broad topic: Scientific Research; Medium topic: Impact of Climate Change; Detailed topic: Polar Regions; \

        # prompt climate posts: 
        user = {
            "role": "user",
            "content": "You will be given a post related to climate change. Please generate topics for the post from different granularities such as broad topic, \
medium topic, and detailed topic, separated by semicolon. Each generated topic should be no more than eight words and you should try to minimize the number of topics generated. \
Here is the post: " + tweet,
        }

        assistant = {
            "role": "assistant",
            "content": broad_topic + medium_topic + detailed_topic
        }

        # if idx in [1, 58, 6, 9, 21, 52, 19, 59, 32, 73, 80, 82]:  # idx starts from 0, but the # in the dataset starts from 1 hence: [2, 59, 7, 10, 22, 53, 20, 60, 33, 74, 81, 83]
        # if num in [70, 4763, 6876, 5790, 2156, 1038, 5151, 5724, 4458, 3646, 4219, 2712, 1057]:       # cyber
        if num in [2429, 1027, 1475, 12320, 5090, 1277, 1503, 6659, 12229, 2068, 5955]:       # climate
            prompt_examples.append(user)
            prompt_examples.append(assistant)

    return prompt_examples


def get_infer_data():
    # df = pd.read_excel('./dataset/covid_posts_togen.xlsx')
    # df = pd.read_excel('./dataset/cyber_posts_togen.xlsx')
    df = pd.read_excel('./dataset/climate_posts_togen.xlsx')
    df.head()
    all_data = []
    infer_data = []
    tweets = []
    n = len(df)
    prompt_examples = get_prompt_examples()

    for idx, row in df.iterrows():
        tweet = row['tweet']
        # covid-19 vaccine 
#         user = {
#             "role": "user",
#             "content": "You will be given a tweet related to Covid-19 vaccine. Please generate topics for the tweet from different granularities such as broad topic, \
# medium topic, and detailed topic, separated by semicolon. Each generated topic should be no more than eight words and you should try to minimize the number of topics generated. \
# Here is a list of existing topics:\
# 1. Broad topic: Government Policies; Medium topic: Vaccine Mandates; Detailed topic: Opposition to Vaccine Mandates; \
# 2. Broad topic: Government Policies; Medium topic: Vaccine Policies; Detailed topic: Vaccine Privacy; \
# 3. Broad topic: Vaccine Safety and Effectiveness; Medium topic: Vaccine Side Effects; Detailed topic: Vaccine-Related Injuries and Deaths; \
# 4. Broad topic: Vaccine Safety and Effectiveness; Medium topic: Vaccine Side Effects; Detailed topic: Myocarditis Side Effect; \
# 5. Broad topic: Vaccine Safety and Effectiveness; Medium topic: Vaccine Side Effects; Detailed topic: Cancer Side Effect; \
# 6. Broad topic: Vaccine Safety and Effectiveness; Medium topic: Scientific and Medical Discussions; Detailed topic: Discussions about Hepatitis; \
# 7. Broad topic: Political and Societal Implications; Medium topic: Conspiracy Theories; \
# 8. Broad topic: Political and Societal Implications; Medium topic: Vaccine Injury; \
# 9. Broad topic: Personal Experiences and Opinions; Medium topic: Vaccine Refusal; \
# 10. Broad topic: Public Opinion; Medium topic: Vaccine Acceptance; \
# 11. Broad topic: Vaccine Distribution and Administration; Medium topic: Vaccine Impact; Detailed topic: Vaccine Impact on Heart Disease; \
# 12. Broad topic: Vaccine Production; Medium topic: Vaccine Manufacturing; Detailed topic: Investigation of  Manufacturers; \
# Please try to generate topics for the tweet using existing topics. If there is no good match, then generate new topics. \
# Here is the post: " + tweet,
#         }

        # cybersecurity
#         user = {
#             "role": "user",
#             "content": "You will be given a Facebook post related to cybersecurity. Please generate topics for the post from different granularities such as broad topic, \
# medium topic, and detailed topic, separated by semicolon. Each generated topic should be no more than eight words and you should try to minimize the number of topics generated. \
# Here is a list of existing topics:\
# 1. Broad topic: Threats; Medium topic: Cyberattacks; Detailed topic: Chinese Cyberattacks on Philippine Websites; \
# 2. Broad topic: Threats; Medium topic: Phishing Attacks; Detailed topic: Phishing Examples; \
# 3. Broad topic: Threats; Medium topic: Data Breaches; Detailed topic: Home Depot Data Breach; \
# 4. Broad topic: Corporate Security; Medium topic: Recycling and Disposal Policies; Detailed topic: IT Equipment Disposal; \
# 5. Broad topic: Corporate Security; Medium topic: Small Business Cybersecurity; \
# 6. Broad topic: Policies and Governance; Medium topic: International Cooperation; Detailed topic: Cybersecurity Partnership Between Slovenia and U.S.; \
# 7. Broad topic: Policies and Governance; Medium topic: Government Regulations; Detailed topic: Challenges in Cybersecurity Information Sharing; \
# 8. Broad topic: Emerging Trends; Medium topic: Cloud Security; Detailed topic: Cloud Repatriation; \
# 9. Broad topic: Emerging Trends; Medium topic: Cybersecurity Events; \
# 10. Broad topic: Security Solutions; Medium topic: Data Protection; Detailed topic: Encrypted USB; \
# 11. Broad topic: Incident Management; Medium topic: Digital Forensics; Detailed topic: Insights into Digital Forensics; \
# 12. Broad topic: Workforce; Medium topic: Leadership; Detailed topic: Leadership Gaps; \
# 13. Broad topic: Education; Medium topic: Cybersecurity Training; Detailed topic: Vulnerability Assessment and Penetration Testing Training; \
# Please try to generate topics for the post using existing topics. If there is no good match, then generate new topics. \
# Here is the post: " + tweet,
#         }

        # climate change
        user = {
            "role": "user",
            "content": "You will be given a post related to climate change. Please generate topics for the post from different granularities such as broad topic, \
medium topic, and detailed topic, separated by semicolon. Each generated topic should be no more than eight words and you should try to minimize the number of topics generated. \
Here is the post: " + tweet,
        }

        tweets.append(tweet)
        infer_data.extend(prompt_examples)
        infer_data.append(user)
        all_data.append(infer_data)
        infer_data = []
        # if idx==2: break   # used for testing

    return all_data, tweets

def convert_msgs_to_str(msgs):
    msgs_str = []
    for msg in msgs:
        msg_str = ""
        for i, m in enumerate(msg):
            if i == len(msg)-1:
                msg_str += "Now answer this: \n Input:\n" + m['content'] + "\n"
                break
            if m['role'] == 'user':
                msg_str += "Example " + str(i//2+1) + ":\n" + "Input:\n" + m['content'] + "\n"
            elif m['role'] == 'assistant':
                msg_str += "Output:\n" + m['content'] + "\n"
        msgs_str.append(msg_str)
    return msgs_str

client = genai.Client(api_key="gemini-api-key")
def predict(msg):
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=msg,
    )
    return response.text

def infer_all():
    msgs, tweets = get_infer_data()
    # print(msgs)
    msgs = convert_msgs_to_str(msgs)
    # for m in msgs:
    #     print(m)
    results = []
    
    # print(msgs[5781])
    # print(len(msgs[5781]))
    # topics = predict(msgs[5781])
    # print(topics)
    i = 0
    while i<len(msgs):
        try:
            msg = msgs[i]  
            print(i, len(msg))
            topics = predict(msg)
            # print(topics)
            topics = topics.split(';')
            if len(topics)>2:
                topics[2] = topics[2].replace("Detailed topic: ", "").lstrip().split("\n")[0]
            if len(topics)>1:
                topics[1] = topics[1].replace("Medium topic: ", "").lstrip()
            if len(topics)>0:
                topics[0] = topics[0].replace("Broad topic: ", "").lstrip()

            output = [tweets[i]] + topics

            results.append(output)
            i += 1
        except Exception as e:
            print("Error:", e)
            time.sleep(60)


    # print(results)

    # with open('./dataset/covid_infer_results_gemini_no_existing.csv', 'w', newline='') as f:
    # with open('./dataset/cyber_infer_results_gemini_no_existing.csv', 'w', newline='') as f:
    with open('./dataset/climate_infer_results_gemini_no_existing.csv', 'w', newline='') as f:
        csvwriter = csv.writer(f, delimiter = ',', lineterminator='\r\n', quotechar='"')
        csvwriter.writerow(["#", "tweet", "broad_topic", "medium_topic", "detailed_topic"])  # , "very_detailed_topic"
        cnt = 1
        for row in results:
            csvwriter.writerow([str(cnt)] + row)
            cnt += 1

    print("Results saved csv file")
    

if __name__ == "__main__":
    infer_all()