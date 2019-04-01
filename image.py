from googleapiclient.discovery import build
import requests
import shutil
import json
import sys

credentials = {}
with open("credentials.json", "r") as file:
    credentials = json.loads(file.read())

# Uses Google's Custom Search Engine to retrieve links to images related to the query
def fetch_images_urls(query, limit=5):
    service = build("customsearch", "v1", developerKey=credentials["google_dev_key"])
    result = service.cse().list(q=query, cx=credentials["search_engine_id"], num=limit, searchType="image", imgSize="large").execute()

    return [item["link"] for item in result["items"]]

# Downloads images from URLs
def download_images(urls):
    n = 1
    for url in urls:
        response = requests.get(url, stream=True)

        with open("image{}.jpg".format(n), 'wb') as image:
            shutil.copyfileobj(response.raw, image)
            n += 1

# Uses Watson Keywords and the original query to fetch images and save to content
def fetch_sentence_images(content):
    for index, sentence in enumerate(content["sentences"]):
        query = content["search_term"] + ' ' + sentence['keywords'][0]
        content["sentences"][index]["google_search_query"] = query
        content["sentences"][index]["images"] = fetch_images_urls(query)
    
    return content

# Main function to be used in the video maker
def image(content):
    return fetch_sentence_images(content)

# Function to search and download images as a standalone script
def main(query, limit=5):
    urls = fetch_images_urls(query, limit=limit)
    download_images(urls)
    print("--- {} images downloaded sucessfully ---".format(limit))

if __name__ == "__main__":
    main(sys.argv[1])