import json
with open('data.json') as json_file:
    data = json.load(json_file)

transcript = data["transcript"]
sentences = words = transcript.split("\n")  
words = data["words"]
i = 0
for sentence in sentences:
    print(sentence)
    for eachword in sentence.split():
        if eachword == words[i]["word"]:
            print(eachword)
            i = i + 1
print(i)