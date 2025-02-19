from openai import OpenAI
import pandas as pd
import csv

OPENAI_API_KEY = 'openai_api_key'
client = OpenAI(api_key=OPENAI_API_KEY)

def predict(msg):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=msg,
        temperature=0.001,
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    df = pd.read_excel('./covid_eval.xlsx')
    df.head()
    A, B = [], []
    for idx, row in df.iterrows():
        claim = row['claim']
        broad_topic = row['broad_topic']
        medium_topic = row['medium_topic']
        detailed_topic = row['detailed_topic']
        
        user = [{
            "role": "user",
            "content": f"""
                I used LLMs to generate topics from three levels for factual claims. Now I need to evaluate ONLY the detailed topics from two aspects: **accuracy** and **granularity**. 
                Here are the two aspects:
                Accuracy: Evaluators will assess how accurately the detailed topics reflect the content and context of the corresponding factual claims. This involves determining if the topics are relevant and if they correctly represent the underlying information without misinterpretation or error.\
                Granularity: This criterion evaluates the specificity of the detailed topics. Evaluators will judge whether the topics are detailed enough to uniquely categorize and differentiate between factual claims, yet broad enough to maintain practical applicability across multiple claims. For example, if a more specific topic level is necessary to bridge the gap between a detailed topic and its corresponding claim, this indicates that the current detailed topic is not sufficiently detailed.
                If there is no detailed topic for a claim then evaluate the medium topic. If there is no medium topic existing, then evaluate broad topic. 

                Please read the evaluation metrics carefully and evaluate the claim-topic pairs and give one score for accuracy and one score for granularity for each claim-topic pair. The score ranges from 1-5, with 5 being the best and 1 being the worst. 

                <<EXAMPLES>>

                <<EXAMPLE 1>>
                Factual claim: I worked for 18 months to end Biden’s unscientific and unethical military COVID vaccine mandate. Thanks to your phone calls and letters, we gained 92 sponsors on HR 3860. Repeal of the mandate just became a reality with the signing of the NDAA. Now let’s end the other mandates. 

                broad topic: Government Policies; medium topic: Vaccine Mandates; detailed topic: Opposition to Vaccine Mandates. 

                Accuracy: 5. Granularity: 5.

                <<EXAMPLE 2>>
                Factual claim: Myocarditis is up TEN times due to the Covid Vaccine... Nearly 30 % of young people have measurable cardiac injuries post-vaccine.. The CDC is LYING about this… 

                broad topic: Vaccine Safety and Effectiveness; medium topic: Vaccine Side Effects; detailed topic: Myocarditis Side Effect 

                Accuracy: 5. Granularity: 5.

                <<EXAMPLE 3>>
                factual claim: Graphen oxide resonates at 26ghz microwaves from a 5G cell towers that’s in the COVID vaccine! You can neutralise the EMF and 5G radiation from mobile devices and detox from heavy metals, learn more here: Covid_19 Agenda2030 AGENDA2030 5GChile ONU. 

                broad topic: Political and Societal Implications; medium topic: Conspiracy Theories

                Accuracy: 5. Granularity: 5.

                <<EXAMPLE 4>>
                factual claim: Study published in Dec. 2020 proved COVID Vaccines could cause Strokes, Alzheimer’s, Parkinson’s, Multiple Sclerosis, and Autoimmune Disorder – Is there any wonder why the Five Eyes &amp; Europe have suffered 2 Million Excess Deaths in the past 2 years? https://t.co/4fOo6P5q3p. 

                broad topic: Vaccine Safety and Effectiveness; medium topic: Scientific and Medical Discussions; detailed topic: Discussions about Strokes, Alzheimer's, Parkinson's, Multiple Sclerosis, and Autoimmune Disorder. 

                Accuracy: 4. Granularity: 2.

                <<EXAMPLE 5>>
                factual claim: 'The doctor said that the probable cause of her heart attack was the vaccine, but he was too scared to put that on the report.' South African politician Jay Naidoo reacts to the South African court being asked to conduct a judicial review of the Covid vaccine. https://t.co/AQgtoy27eI. 

                broad topic: Political and Societal Implications; medium topic: Vaccine Injury; detailed topic: Court Review of Covid Vaccine.

                Accuracy: 2. Granularity: 5.
                <<END EXAMPLES>>

                Now, please evaluate the topics for the following claim-topic pairs and only provide the scores for accuracy and granularity separated by a comma. For example. 3, 4.
                Claim: {claim}
                Broad Topic: {broad_topic}
                Medium Topic: {medium_topic}
                Detailed Topic: {detailed_topic}
            """
        }]
        ans = predict(user)
        print(ans)
        a, b = ans.split(',')
        A.append(a)
        B.append(b)
    # add A and B to the dataframe
    df['accuracy'] = A
    df['granularity'] = B
    df.to_csv('./covid_eval_results.csv', index=False)
