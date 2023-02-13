from textblob import TextBlob
from nltk.corpus import stopwords

def audioExtractSymptomsRaw():
    sentence=''

    with open("audioToText.txt",'r') as tfile:
        sentence = tfile.read()


    stop_words = set(stopwords.words('english'))

    blob = TextBlob(sentence)

    symptoms = []
    for i, (word, pos) in enumerate(blob.tags):
        if word in stop_words:
            continue
        if pos in ["JJ", "IN", "NN","NNS","VBN"]:
            if i+1 < len(blob.tags) and blob.tags[i+1][1] == "NN":
                if word + " " + blob.tags[i+1][0] not in symptoms:
                    symptoms.append(word + "_" + blob.tags[i+1][0])
            else:
                if word not in symptoms:
                    symptoms.append(word)

    return symptoms