from watson_developer_cloud import NaturalLanguageUnderstandingV1
from nltk import sent_tokenize

import Algorithmia
import json
import re

def fetch_wikipedia_article(content):
    algorithmia_key = ""
    with open("credentials.json", "r") as file:
        algorithmia_key = json.loads(file.read())["algorithmia_key"]

    client = Algorithmia.client('simAoS+NCBot8SACwnHwpY0ezGR1')   
    algo = client.algo('web/WikipediaParser/0.1.2')  
    content["source_original_content"] = algo.pipe(content['search_term']).result["content"]
    return content

# Removes blank lines, dates in paretheses, and whatever is left of Markdown
def sanitize_content(content):
    article = content['source_original_content']

    # Removes blank lines and markdown
    article = "".join([i for i in article.splitlines(True) if not (len(i) < 2 or i.startswith('='))])

    # Removes dates in parentheses
    article = re.sub("/\((?:\([^()]*\)|[^()])*\)/gm", '', article)

    content["source_sanitized_content"] = article
    return content

# Uses IBM Cloud Natural Language Understanding API to analyze the sentences and get keywords
def watson_keywords(sentence):
    watson_key = ""
    with open("credentials.json", "r") as file:
        watson_key = json.loads(file.read())["watson_key"]

    nlu = NaturalLanguageUnderstandingV1('2018-04-05', iam_apikey=watson_key)
    analysis = nlu.analyze(features={"keywords":{}}, text=sentence).get_result()
    return [i["text"] for i in analysis["keywords"]]


# Breaks the content into understandable sentences
def break_into_sentences(content, limit=10):
    content["sentences"] = []
    
    for sentence in sent_tokenize(content["source_sanitized_content"])[:limit]:
        content["sentences"].append({'text':sentence, 'keywords':watson_keywords(sentence), 'images':[]})
    
    return content

def text(content, max_sentences=10):
    content = fetch_wikipedia_article(content)
    content = sanitize_content(content)
    content = break_into_sentences(content, max_sentences)

    return content