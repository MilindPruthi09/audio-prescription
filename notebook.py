import csv
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from collections import defaultdict

def firstpart():
    disease_list = []

    def return_list(disease):
        disease_list = []
        match = disease.replace('^','_').split('_') # using _ as common splitting delimeter
        ctr = 1
        for group in match:
            if ctr%2==0:
                disease_list.append(group) # refer the data format
            ctr = ctr + 1

        return disease_list

    with open("./Model/raw_data_2.csv") as csvfile:
        reader = csv.reader(csvfile)
        disease=""
        weight = 0
        disease_list = []
        dict_wt = {}
        dict_=defaultdict(list)
        
        for row in reader:

            if row[0]!="\xc2\0xa0" and row[0]!="": # for handling file encoding errors
            # saving disease and frequency
                disease = row[0]
                disease_list = return_list(disease)
                weight = row[1]

            if row[2]!="\xc2\0xa0" and row[2]!="":
                symptom_list = return_list(row[2])

                for d in disease_list:
                    for s in symptom_list:
                        dict_[d].append(s) # adding all symptoms
                    dict_wt[d] = weight

    with open("./Model/dataset_clean.csv","w") as csvfile:
        writer = csv.writer(csvfile)
        for key,values in dict_.items():
            for v in values:
                #key = str.encode(key)
                key = str.encode(key).decode('utf-8')
                #.strip()
                #v = v.encode('utf-8').strip()
                #v = str.encode(v)
                writer.writerow([key,v,dict_wt[key]])

    columns = ['Source','Target','Weight'] # source: disease, target: symptom, weight: number of cases

    data = pd.read_csv("./Model/dataset_clean.csv",names=columns, encoding ="ISO-8859-1")
    data.to_csv("./Model/dataset_clean.csv",index=False)
    data = pd.read_csv("./Model/dataset_clean.csv", encoding ="utf-8")

    df = pd.DataFrame(data)
    df_1 = pd.get_dummies(df.Target) # 1 hot encoding symptoms
    df_s = df['Source']

    df_pivoted = pd.concat([df_s,df_1], axis=1)
    df_pivoted.drop_duplicates(keep='first',inplace=True)

    cols = df_pivoted.columns

    cols = cols[1:] # removing headings

    df_pivoted = df_pivoted.groupby('Source').sum()
    df_pivoted = df_pivoted.reset_index()

    df_pivoted.to_csv("./Model/df_pivoted.csv")

    x = df_pivoted[cols]
    y = df_pivoted['Source']

    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)

    # Training multinomial naive bayes
    mnb = MultinomialNB()
    mnb = mnb.fit(x_train, y_train)
    #mnb.score(x_test, y_test)

    mnb_tot = MultinomialNB()
    mnb_tot = mnb_tot.fit(x, y)

    mnb_tot.score(x, y)


    disease_pred = mnb_tot.predict(x)

    disease_real = y.values

    # printing model error
    for i in range(0, len(disease_real)):
        if disease_pred[i]!=disease_real[i]:
            print ('Pred: {0} Actual:{1}'.format(disease_pred[i], disease_real[i]))

    from sklearn.tree import DecisionTreeClassifier, export_graphviz


    dt = DecisionTreeClassifier()
    clf_dt=dt.fit(x,y)
    print ("DT Acurracy: ", clf_dt.score(x,y))


    from sklearn import tree 
    from sklearn.tree import export_graphviz

    export_graphviz(dt, 
                    out_file='tree.jpg', 
                    feature_names=cols
                )


    data = pd.read_csv("./Model/Training.csv")

    symptoms_f=data.columns
    with open("full_symptoms.txt",'w') as tfile:
        for items in symptoms_f:
            tfile.write(items+',')

def secondpart():
    data = pd.read_csv("./Model/Training.csv")
    df = pd.DataFrame(data)

    cols = df.columns
    cols = cols[:-1]

    x = df[cols]
    y = df['prognosis']


    # x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)

    # mnb = MultinomialNB()
    # mnb = mnb.fit(x_train, y_train)

    # mnb.score(x_test, y_test)

    # from sklearn import model_selection
    # print ("cross result========")
    # scores = model_selection.cross_val_score(mnb, x_test, y_test, cv=3)
    # print (scores)
    # print (scores.mean())

    test_data = pd.read_csv("./Model/Testing.csv")

    testx = test_data[cols]
    testy = test_data['prognosis']


    # mnb.score(testx, testy)

    # from sklearn import model_selection
    # print ("cross result========")
    # scores = model_selection.cross_val_score(mnb, x_test, y_test, cv=3)
    # print (scores)
    # print (scores.mean())


    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)

    print ("DecisionTree")
    dt = DecisionTreeClassifier(min_samples_split=20)
    clf_dt=dt.fit(x_train,y_train)
    print ("Acurracy: ", clf_dt.score(x_test,y_test))



    from sklearn import model_selection
    print ("cross result========")
    scores = model_selection.cross_val_score(dt, x_test, y_test, cv=3)
    print (scores)
    print (scores.mean())



    print ("Acurracy on the actual test data: ", clf_dt.score(testx,testy))

    from sklearn import tree 
    from sklearn.tree import export_graphviz

    export_graphviz(dt, 
                    out_file='tree.dot', 
                    feature_names=cols)


    dt.__getstate__()


    importances = dt.feature_importances_

    indices = np.argsort(importances)[::-1]

    features = cols

    # for f in range(20):
    #     print("%d. feature %d - %s (%f)" % (f + 1, indices[f], features[indices[f]] ,importances[indices[f]]))

    export_graphviz(dt, 
                    out_file='tree-top5.dot', 
                    feature_names=cols,
                    max_depth = 5
                )


    feature_dict = {}
    for i,f in enumerate(features):
        feature_dict[f] = i

    feature_dict['internal_itching']



    sample_x = [i/52 if i==52 else i*0 for i in range(len(features))]
    cols = list(data.columns) 

    sample_x = np.array(sample_x).reshape(1,len(sample_x))

    dt.predict(sample_x)


    dt.predict_proba(sample_x)

    symptoms = ['skin_rash','itching','nodal_skin_eruptions','increased_appetite','irritability']
    ipt = [0 for i in range(len(features))]
    for s in symptoms:
        ipt[cols.index(s)]=1
    print("-------------------------------------------------------------------------",len(ipt))
    ipt = np.array([ipt])
    print(ipt)
    print(dt.predict(ipt))
    dt.predict_proba(ipt)

firstpart()
secondpart()