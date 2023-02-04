import csv
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from collections import defaultdict
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_graphviz

disease_list = []

def return_list(disease):
    disease_list = []
    match = disease.replace('^','_').split('_')
    ctr = 1
    for group in match:
        if ctr%2==0:
            disease_list.append(group)
        ctr = ctr + 1

    return disease_list

with open("Model/raw_data_2.csv") as csvfile:
    reader = csv.reader(csvfile)
    disease=""
    weight = 0
    disease_list = []
    dict_wt = {}
    dict_=defaultdict(list)
    
    for row in reader:

        if row[0]!="\xc2\0xa0" and row[0]!="":
            disease = row[0]
            disease_list = return_list(disease)
            weight = row[1]

        if row[2]!="\xc2\0xa0" and row[2]!="":
            symptom_list = return_list(row[2])

            for d in disease_list:
                for s in symptom_list:
                    dict_[d].append(s)
                dict_wt[d] = weight

with open("dataset_clean.csv","w") as csvfile:
    writer = csv.writer(csvfile)
    for key,values in dict_.items():
        for v in values:
            key = str.encode(key).decode('utf-8')
            writer.writerow([key,v,dict_wt[key]])

columns = ['Source','Target','Weight']

data = pd.read_csv("dataset_clean.csv",names=columns, encoding ="ISO-8859-1")
data.to_csv("dataset_clean.csv",index=False)
data = pd.read_csv("dataset_clean.csv", encoding ="ISO-8859-1")

df = pd.DataFrame(data)
df_1 = pd.get_dummies(df.Target)
df_s = df['Source']

df_pivoted = pd.concat([df_s,df_1], axis=1)
df_pivoted.drop_duplicates(keep='first',inplace=True)

cols = df_pivoted.columns
cols = cols[1:]

df_pivoted = df_pivoted.groupby('Source').sum()
df_pivoted = df_pivoted.reset_index()
df_pivoted[:5]
df_pivoted.to_csv("df_pivoted.csv")

x = df_pivoted[cols]
y = df_pivoted['Source']

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=42)

dt = DecisionTreeClassifier(min_samples_split=20)
clf_dt=dt.fit(x_train,y_train)

importances = dt.feature_importances_
print(dt.feature_importances_)

features = cols

symptoms = ['skin_rash','itching','nodal_skin_eruptions','increased_appetite','irritability']
ipt = [0 for i in range(len(features))]
for s in symptoms:
  ipt[cols.index(s)]=1
ipt = np.array([ipt])
print(ipt)
print(dt.predict(ipt))
dt.predict_proba(ipt)