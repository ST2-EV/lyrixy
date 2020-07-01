import json
with open('data.json') as json_file:
    data = json.load(json_file)

transcript = data["transcript"]
sentences = words = transcript.split("\n")  
words = data["words"]
