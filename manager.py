from text import *

def get_user_input():
    content["search_term"] = input("Type a Wikipedia query: ")

    prefixes = ['Who is', 'What is', 'The history of']
    print("Choose one of the options:", *["[{}] {}".format(i, j) for i, j in enumerate(prefixes)], sep="\n")
    prefix_index = int(input())

    content["prefix"] = prefixes[prefix_index]

    return content

def main():
    content = get_user_input()
    content = text(content)

if __name__ == "__main__":
    main()
