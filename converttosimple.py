def breakdown():
    with open("audioToText.txt",'r') as tfile:
            sentence = tfile.read()
    lst=[]
    sentence=sentence.split(' and ')
    for sentences in sentence:
            lst.append([sentences])
    return lst