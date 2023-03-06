def utility():
    with open('full_symptoms.txt', 'r') as file:
       data = file.read()
    data=data.replace(","," ")
    data=data.strip()
    data=data.split(" ")
    ls=[]
    data = list(filter(None, data))
    for item in data:
        items=item.split("_")
        ls.append(list(filter(None, items)))
    newList = list(filter(None, ls))
    return newList

utility()