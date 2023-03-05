from converttosimple import *
from MachineModel import *
from full_symptoms_2D import *

with open('full_symptoms.txt', 'r') as file:
    data = file.read()
data=data.replace(","," ")
data=data.split(" ")
split_data = [i.split("_") for i in data]
flat_data = [word for sublist in split_data for word in sublist]

lst=breakdown()
final_symptoms_breakdown=[]

for item in lst:
    sent=''.join(item)
    useraudioraw = audioExtractSymptomsRaw(sent)
    final_symptoms_breakdown.append(useraudioraw)

debug=[]
passer=''
for items in final_symptoms_breakdown:
    for item in items:
        if item in flat_data:
            passer=passer+' '+item
    debug.append(passer.strip().split(' '))
    passer=''

data_symptoms = debug
final_Symptom_List_2D = utility()
