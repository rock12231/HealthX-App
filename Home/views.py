from django.shortcuts import render
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
import pandas as pd
import joblib
from Profile.models import ProfileModel


# Read data from csv file
df = pd.read_csv("Home/data/heart.csv", on_bad_lines='skip')
# print(df.head(5))
# print(type(df))
# model = pickle.load(open('selectCar/data/deepmodel.sav', "rb"))
# loaded_model = joblib.load('Home/data/model1.sav')

# input_data = (53,1,0,140,203,1,0,155,1,3,1,0,0)
# prediction = loaded_model.predict([input_data])

# if prediction[0] == 0:
    # print('>>>>>>The Person does not have Heart Disease')
# else:
    # print('>>>>>>The Person has Heart Disease')


class Home(View):
    def get(self,request):
        chest_pain = {
            'total' : len(df.index),
            'chest_pain': len(df[df['cp'] == 0]),
            'chest_pain1': len(df[df['cp'] == 1]),
            'chest_pain2': len(df[df['cp'] == 2]),
            'chest_pain3': len(df[df['cp'] == 3]),
        }
        
        context = {
            'total_record':len(df.index),
            # 'total_patient': len(df[df['target'] == 1]),
            'total_patient': ProfileModel.objects.count(),
            'total_male': len(df[df['sex'] == 1]),
            'total_female': len(df[df['sex'] == 0]),
            'chest_pain' : chest_pain,   
        }
        return render(request, 'Home/index.html', context)

