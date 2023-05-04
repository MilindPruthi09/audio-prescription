from textblob import TextBlob
from nltk.corpus import stopwords

def audioExtractSymptomsRaw(sentence):
    stop_words = set(stopwords.words('english'))

    blob = TextBlob(sentence)

    symptoms = []
    for i, (word, pos) in enumerate(blob.tags):
        if word in stop_words:
            continue
        if pos in ["JJ", "IN", "NN","NNS","VBN","VBZ","VBP","VBN","VBG","VBD","VB"]:
            if i+1 < len(blob.tags) and blob.tags[i+1][1] == "NN":
                symptoms.append(word)
            else:
                if word not in symptoms:
                    symptoms.append(word)

    return symptoms