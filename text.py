from watson_developer_cloud import NaturalLanguageUnderstandingV1
from nltk import sent_tokenize

import pprint as pp
import Algorithmia
import re

def fetch_wikipedia_article(content):
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
    nlu = NaturalLanguageUnderstandingV1('2018-04-05', iam_apikey="DT_MSscAMP6nZkLPTCAvf3z3gPA1smlt-GTwA6ewGqaD")
    analysis = nlu.analyze(features={"keywords":{}}, text=sentence).get_result()
    return [i["text"] for i in analysis["keywords"]]


# Breaks the content into understandable sentences
def break_into_sentences(content):
    content["sentences"] = []
    
    for sentence in sent_tokenize(content["source_sanitized_content"]):
        content["sentences"].append({'text':sentence, 'keywords':watson_keywords(sentence), 'images':[]})
    
    return content

def text(content):
    content = fetch_wikipedia_article(content)
    content = sanitize_content(content)
    content = break_into_sentences(content)

    return content