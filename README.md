
# LLMTaxo

## Note
Due to the privacy issue of social media platforms, we only release tweet id for COVID-19 vaccine dataset. 

The final taxonmies are privided in "taxonomy" folder.

![LLMTaxo Framework](./framework.png)

## Create the Environment
conda env create -f environment.yml

## Perform the Framework
We follow the steps in the framework to build the taxonomy.

### Data Preprocessing
Load data and retrive social media posts that have a ClaiimBuster score > 0.5

`python posts_preprocess.py`

### Clustering

`python clustering.py`

### Identifying Distinct Claim

`python posts_for_topic_generation.py`

### Topic Generation

`python zephyr_infer.py`
`python gpt_infer.py`

### Taxonomy Construction

`python build_taxonomy.py`

### GPT Evaluation

`python gpt_evaluation.py`

