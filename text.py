from watson_developer_cloud import NaturalLanguageUnderstandingV1
from nltk import sent_tokenize
from store import save, load

import Algorithmia
import json
import re

def fetch_wikipedia_article():
    content = load()
    
    algorithmia_key = ""
    with open("credentials.json", "r") as file:
        algorithmia_key = json.loads(file.read())["algorithmia_key"]

    client = Algorithmia.client(algorithmia_key)   
    algo = client.algo('web/WikipediaParser/0.1.2')  
    
    content["source_original_content"] = algo.pipe(content['search_term']).result["content"]

    save(content)

# Removes blank lines, dates in paretheses, and whatever is left of Markdown
def sanitize_content():
    content = load()

    article = content['source_original_content']

    # Removes blank lines and markdown
    article = "".join([i for i in article.splitlines(True) if not (len(i) < 2 or i.startswith('='))])

    # Removes dates in parentheses
    article = re.sub("/\((?:\([^()]*\)|[^()])*\)/gm", '', article)

    content["source_sanitized_content"] = article
    
    save(content)

# Uses IBM Cloud Natural Language Understanding API to analyze the sentences and get keywords
def watson_keywords(sentence):
    watson_key = ""
    with open("credentials.json", "r") as file:
        watson_key = json.loads(file.read())["watson_key"]

    nlu = NaturalLanguageUnderstandingV1('2018-04-05', iam_apikey=watson_key)
    analysis = nlu.analyze(features={"keywords":{}}, text=sentence).get_result()
    return [i["text"] for i in analysis["keywords"]]


# Breaks the content into understandable sentences
def break_into_sentences(limit=5):
    content = load()

    content["sentences"] = []
    
    for sentence in sent_tokenize(content["source_sanitized_content"])[:limit]:
        content["sentences"].append({'text':sentence, 'keywords':watson_keywords(sentence), 'images':[]})
    
    save(content)

def text(max_sentences=5):
    fetch_wikipedia_article()
    sanitize_content()
    break_into_sentences(max_sentences)
