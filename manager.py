from image import *
from store import *
from text import *

import json

def get_user_input():
    content = {}
    content["search_term"] = input("Type a Wikipedia query: ")

    prefixes = ['Who is', 'What is', 'The history of']
    print("Choose one of the options:", *["[{}] {}".format(i, j) for i, j in enumerate(prefixes)], sep="\n")
    prefix_index = int(input())

    content["prefix"] = prefixes[prefix_index]

    save(content)


def main():
    get_user_input()
    text()
    image()

if __name__ == "__main__":
    main()
