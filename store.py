import json

def save(data):
    with open("content.json", 'w') as file:
        json.dump(data, file, indent=4, sort_keys=True)

def load():
    data = {}
    with open("content.json", 'r') as file:
        data = json.loads(file.read())

    return data