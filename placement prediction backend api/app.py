import uvicorn
from fastapi import FastAPI
from attrName import attrName
import numpy as np
import pickle
import pandas as pd

app = FastAPI()

LG = open("placpredModelLG.pkl", 'rb')
LGmodel = pickle.load(LG)

KNN = open("placpredModelKNN.pkl", 'rb')
KNNmodel = pickle.load(KNN)

NB = open("placpredModelNB.pkl", 'rb')
NBmodel = pickle.load(NB)

SVM = open("placpredModelSVM.pkl", 'rb')
SVMmodel = pickle.load(SVM)

RF = open("placpredModelRandFor.pkl", 'rb')
RFmodel = pickle.load(RF)


@app.get('/')
def index():
    return {
        'message' : "Hello, Stranger"
    }
@app.post('/predict')
def predict_placement(data: attrName):
    data = dict(data)
    print(data)
    Age = int(data['Age'])
    Gender = int(data['Gender'])
    Stream = int(data['Stream'])
    Internships = int(data['Internships'])
    CGPA = float(data['CGPA'])
    Hostel = int(data['Hostel'])
    HistoryOfBacklogs = int(data['HistoryOfBacklogs'])
    projectsCount = int(data['projectsCount'])

    prediction_from_models = []

    prediction_from_models.append(LGmodel.predict([[Age, Gender, Stream, Internships, CGPA, Hostel, HistoryOfBacklogs, projectsCount]])[0])
    prediction_from_models.append(KNNmodel.predict([[Age, Gender, Stream, Internships, CGPA, Hostel, HistoryOfBacklogs, projectsCount]])[0])
    prediction_from_models.append(NBmodel.predict([[Age, Gender, Stream, Internships, CGPA, Hostel, HistoryOfBacklogs, projectsCount]])[0])
    prediction_from_models.append(SVMmodel.predict([[Age, Gender, Stream, Internships, CGPA, Hostel, HistoryOfBacklogs, projectsCount]])[0])
    prediction_from_models.append(RFmodel.predict([[Age, Gender, Stream, Internships, CGPA, Hostel, HistoryOfBacklogs, projectsCount]])[0])

    sum = 0

    predication_of_placement = ""

    for i in prediction_from_models:
        sum += i

    if sum == 0 or sum == 1:
        predication_of_placement = "You won't get placed."
    elif sum == 2:
        predication_of_placement = "You are most likely to not get placed."
    elif sum == 3:
        predication_of_placement = "You are likely to get placed."
    elif sum == 4 or sum == 5:
        predication_of_placement = "You will surely get placed"
    else:
        predication_of_placement = "Not Sure"


    print(predication_of_placement)

    value = {
        'prediction_of_placement': predication_of_placement,
        'no_of_true': int(sum)
    }

    return value





if __name__=="__main__":
    uvicorn.run(app, host='127.0.0.1', port=8000)


#uvicorn app:app --reload