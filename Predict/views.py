from django.shortcuts import render
from django.views import View
from Profile.models import ProfileModel
from Predict.models import ChatModel
import joblib
from Home.views import df
import pandas as pd
import os
import csv
import google.generativeai as genai
from dotenv import load_dotenv
genai.configure(api_key=os.getenv('Gemini_API'))

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
        # patient = ProfileModel.objects.get(link=link)
        chats = ChatModel.objects.all()
        ai_prescription = ''
        if request.method == 'POST':
            if request.POST.get("form_type") == 'formOne':
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
            if request.POST.get("form_type") == 'formTwo':
                    print('formTwo')
                    print(request.user.username)
                    csv_file_path = f'BaseAPI/data/vipin.csv'
                    if not os.path.isfile(csv_file_path):
                        # Create a new file and write data to it
                        with open(csv_file_path, 'w', newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(['age','sex','cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal'])        
                    patient_df = pd.read_csv(csv_file_path, on_bad_lines='skip')
                    
                    generation_config = {
                    "temperature": 0.2,
                    "top_p": 0.95,
                    "top_k": 0,
                    "max_output_tokens": 8192,
                    }
                    safety_settings = [
                    {
                        "category": "HARM_CATEGORY_HARASSMENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_HATE_SPEECH",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    {
                        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
                    },
                    ]

                    model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                                                generation_config=generation_config,
                                                safety_settings=safety_settings)

                    convo = model.start_chat(history=[
                        
                    ])
                    patient_details =patient_df.to_string()

                    print("+++++++++++++++++++++++++")
                    print(patient_details)
                    print("+++++++++++++++++++++++++")
                    convo.send_message("You're a professional heart specialist doctor, you're provided with the task to analyze the heart feature data and provide the response in the json format contaning the header - Reasoning, Remedies, Action_to_Take.The provided data is sufficient to take a judgement on. The data of the patient is here - {patient_details}. You're a doctor and don't provide the disclamair or any additional information, only the json is required. Don't mention anything about the insufficient Data.")
                    print(convo.last.text)

                    ai_prescription = convo.last.text
        chats = ChatModel.objects.all()

     
        return render(request, 'Predict/prescription.html', {'chats': chats, 'ai_prescription': ai_prescription})
    