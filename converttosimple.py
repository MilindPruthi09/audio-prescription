def breakdown():
    with open("audioToText.txt",'r') as tfile:
            sentence = tfile.read()
    lst=[]
    sentence=sentence.split('. ')
    for sentences in sentence:
            if('and' in sentences):
                  p=sentences.split(' and ')
                  lst.append(p)
            else:
                lst.append(sentences)
    flattened_list = [item for sublist in lst for item in (sublist if isinstance(sublist, list) else [sublist])]
    return flattened_list