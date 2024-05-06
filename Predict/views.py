from django.shortcuts import render
from django.views import View
from Profile.models import ProfileModel
from Predict.models import ChatModel
import joblib
from Home.views import df
import pandas as pd
import os
import csv


# Create your views here.
loaded_model = joblib.load('Home/data/model1.sav')

class Prediction(View):
    def get(self,request,link):
        patient = ProfileModel.objects.get(link=link)
        print(patient)
        print(patient.age)
        print(patient.sex)
        csv_file_path = f'BaseAPI/data/{patient}.csv'
        # file_exists = os.path.isfile(csv_file_path)
        if not os.path.isfile(csv_file_path):
            # Create a new file and write data to it
            with open(csv_file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal'])        
        patient_df = pd.read_csv(csv_file_path, on_bad_lines='skip')
        # add columns to the patient_df sex and age 
        tempdf = patient_df.head()
        print(tempdf)
        tempdf['age'] = patient.age
        tempdf['sex'] = patient.sex
        tempdf = tempdf.reindex(columns=['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal'])
        # copy dataframes
        final = tempdf.copy()
        for i in range(len(tempdf)):
            # Make list from each row like [53,1,0,140,203,1,0,155,1,3,1,0,0]
            list_data = tempdf.iloc[i].tolist()
            print(list_data)
            prediction = loaded_model.predict([list_data])
            final['target'] = prediction[0]
            
        print(final.head())
        
        context = {
            'data': final.head(5),
            'patient': patient,
            'status': patient.status
        }
        return render(request, 'Predict/prediction.html', context)
    
    def post(self, request, link):
        # already have the column names : age sex 
        # ['age' 'sex' 'cp' 'trestbps' 'chol' 'fbs' 'restecg' 'thalach' 'exang' 'oldpeak' 'slope' 'ca' 'thal']
        if request.method == 'POST':
            # obj = ProfileModel.objects.get(user=user)
            # age = obj.age
            # sex = obj.sex
            patient = ProfileModel.objects.get(link=link)
            age = patient.age
            sex = patient.sex
            cp = int(request.POST['cp'])
            trestbps = int(float(request.POST['trestbps']))
            chol = int(request.POST['chol'])
            fbs = int(request.POST['fbs'])
            restecg = int(request.POST['restecg'])
            thalach = int(request.POST['thalach'])
            exang = int(request.POST['exang'])
            oldpeak = float(request.POST['oldpeak'])
            slope = int(request.POST['slope'])
            ca = int(request.POST['ca'])
            thal = int(request.POST['thal'])  
            print(age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal)         
            # input_data = (53,1,0,140,203,1,0,155,1,3,1,0,0)
            input_data = (age,sex,cp,trestbps,chol,fbs,restecg,thalach,exang,oldpeak,slope,ca,thal)
            print(input_data)
            prediction = loaded_model.predict([input_data])
            if prediction[0] == 0:
                result = '>>>>>  The Person does not have Heart Disease  <<<<<'
                val = 0
                print('>>>>>  The Person does not have Heart Disease  <<<<<')
            else:
                result = '>>>>> The Person has Heart Disease <<<<<'
                val = 1
                print('>>>>>>The Person has Heart Disease')  
        context = {
            'data': df.head(5),
            'prediction': prediction[0],
            'val' : val,
            'result': result
        }    
        return render(request, 'Predict/prediction.html', context)

class Prescription(View):
    def get(self,request, link):
        chats = ChatModel.objects.all()
        return render(request, 'Predict/prescription.html', {'chats': chats})
    
    def post(self, request, link):  
        chats = ChatModel.objects.all()
        for chat in chats:
            print(chat.user, chat.message)   
        if request.method == 'POST':
            message = request.POST.get('chat','')  # Retrieve the message from the POST data
            print(message)
            if message:  # Check if the message is not empty
                user = request.user
                if request.user.is_staff:
                    type = 1
                else:
                    type = 0
                chat = ChatModel(user=user,type=type, message=message)
                chat.save()
        chats = ChatModel.objects.all()
        return render(request, 'Predict/prescription.html', {'chats': chats})
    