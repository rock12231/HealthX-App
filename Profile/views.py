from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from Profile.models import ProfileModel,Notification
# Create your views here.
from Home.views import df
import pandas as pd
import os
import csv
import logging
from Profile.models import UserActivityLog

logger = logging.getLogger('user_activity_logger')

class Login(View):
    def get(self,request):
        return render(request, 'Profile/login.html')
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        print(username,password)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # log_user_activity(request, 'Login')
            if self.request.user.is_superuser : 
                return redirect('admin:index')
            elif self.request.user.is_staff : 
                return redirect('doctor')
            else:
                return redirect('patient')
        else:
            messages.error(request, 'Invalid Credentials')
            return render(request, 'Profile/login.html')
        
        
class Patient(View):
    
    def get(self,request):
        try:
            profile = ProfileModel.objects.get(user=request.user)
        except ProfileModel.DoesNotExist:
            profile = ProfileModel.objects.create(user=request.user, status='pending', link='')
        profile.save()
        csv_file_path = f'BaseAPI/data/{profile}.csv'
        if not os.path.isfile(csv_file_path):
            with open(csv_file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal'])        
        patient_df = pd.read_csv(csv_file_path, on_bad_lines='skip')

        chest_pain = {
            'total' : len(df.index),
            'chest_pain': len(df[df['cp'] == 0]),
            'chest_pain1': len(df[df['cp'] == 1]),
            'chest_pain2': len(df[df['cp'] == 2]),
            'chest_pain3': len(df[df['cp'] == 3]),
        }
        user_notification = NotificationFun(request.user)
        context = {
            'chest_pain' : chest_pain,
            'data': patient_df.head(5),
            'age': profile.age,
            'sex': profile.sex,
            'Notifications': user_notification,
         }
        return render(request, 'Profile/patient.html', context)

    def post(self, request):
        age = request.POST['age']
        sex = request.POST['sex'] 
        print(age,sex) 
        try:
            profile = ProfileModel.objects.get(user=request.user)
            profile.age = age
            profile.sex = sex
            print("try block")
        except ProfileModel.DoesNotExist:
            profile = ProfileModel.objects.create(user=request.user, age=age, sex=sex, status='pending', link='')
            print("except block")
            # csv_file_path = f'BaseAPI/data/{request.user}.csv'
            # # Check if the file exists
            # if not os.path.isfile(csv_file_path):
            #     # Create a new file and write data to it
            #     with open(csv_file_path, 'w', newline='') as file:
            #         writer = csv.writer(file)
            #         writer.writerow(['cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal'])
        
        profile.save()
           
        newdata = ProfileModel.objects.get(user=request.user)
        
        csv_file_path = f'BaseAPI/data/{profile}.csv'
        patient_df = pd.read_csv(csv_file_path, on_bad_lines='skip')
        
        chest_pain = {
            'total' : len(df.index),
            'chest_pain': len(df[df['cp'] == 0]),
            'chest_pain1': len(df[df['cp'] == 1]),
            'chest_pain2': len(df[df['cp'] == 2]),
            'chest_pain3': len(df[df['cp'] == 3]),
        }
        
        context = {
            'chest_pain' : chest_pain,
            'data': patient_df.head(5),
            'age': newdata.age,
            'sex': newdata.sex
        }
        return render(request, 'Profile/patient.html', context)
       
       
class Doctor(View):
    def get(self,request):
        user_profile_data = []
        # Get all active users not staff and superuser
        All_patients = User.objects.filter(is_active=True).exclude(is_staff=True).exclude(is_superuser=True)
        # print(All_patients)
        All_profiles = ProfileModel.objects.exclude(age__lte=0)
        for patient in All_patients:
            try:
                # profile = ProfileModel.objects.get(user=patient)
                profile = All_profiles.get(user=patient)
                user_data = {
                    'id': patient.id,
                    'link' : profile.link,
                    'sex' : profile.sex,
                    'username': patient.username,
                    'status': profile.status,
                    'date_joined': patient.date_joined,
                    'last_login': patient.last_login,
                }
                user_profile_data.append(user_data)
            except ProfileModel.DoesNotExist:
                pass

        chest_pain = {
            'total' : len(df.index),
            'chest_pain': len(df[df['cp'] == 0]),
            'chest_pain1': len(df[df['cp'] == 1]),
            'chest_pain2': len(df[df['cp'] == 2]),
            'chest_pain3': len(df[df['cp'] == 3]),
        }
        print(">>>>>>",user_profile_data)
        context = {
            'total_record':len(df.index),
            'total_patient': ProfileModel.objects.count(),
            'total_male': len(df[df['sex'] == 1]),
            'total_female': len(df[df['sex'] == 0]),
            'chest_pain' : chest_pain, 
            'patients': user_profile_data,  
        }
        return render(request, 'Profile/doctor.html', context)

    def post(self, request):
        status = request.POST['status']
        uid = request.POST['uid']
        try:
            profile = ProfileModel.objects.get(id=uid)
            profile.status = status
            profile.save()
            print("try block")
        except ProfileModel.DoesNotExist:
            print("except block")
            
        print(request.POST,">>>>>>>>>>>")
        user_profile_data = []
        # Get all active users not staff and superuser
        All_patients = User.objects.filter(is_active=True).exclude(is_staff=True).exclude(is_superuser=True)
        # print(All_patients)
        All_profiles = ProfileModel.objects.exclude(age__lte=0)
        for patient in All_patients:
            try:
                # profile = ProfileModel.objects.get(user=patient)
                profile = All_profiles.get(user=patient)
                user_data = {
                    'id': patient.id,
                    'link' : profile.link,
                    'sex' : profile.sex,
                    'username': patient.username,
                    'status': profile.status,
                    'date_joined': patient.date_joined,
                    'last_login': patient.last_login,
                }
                user_profile_data.append(user_data)
            except ProfileModel.DoesNotExist:
                pass

        chest_pain = {
            'total' : len(df.index),
            'chest_pain': len(df[df['cp'] == 0]),
            'chest_pain1': len(df[df['cp'] == 1]),
            'chest_pain2': len(df[df['cp'] == 2]),
            'chest_pain3': len(df[df['cp'] == 3]),
        }
        
        context = {
            'total_record':len(df.index),
            'total_patient': ProfileModel.objects.count(),
            'total_male': len(df[df['sex'] == 1]),
            'total_female': len(df[df['sex'] == 0]),
            'chest_pain' : chest_pain, 
            'patients': user_profile_data,  
        }
        return render(request, 'Profile/doctor.html', context)
        

# Register
class Register(View):
    def get(self, request):
        return render(request, 'Profile/register.html')
    
    def post(self, request):
        try:
            username = request.POST['username']
            email = request.POST['email']
            password = request.POST['password']
            data = User.objects.create_user(username=username, email=email, password=password)
            data.save()
            messages.success(request, 'Account created Successfully')
            
            return redirect('login')
        except:
            messages.success(request, 'Please Retry')
            return render(request, 'Profile/register.html')
        
        
class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('home')

def NotificationFun(user):
    notification = Notification.objects.filter(user=user)
    notification_count = Notification.objects.filter(user=user, is_read=False).count()
    return {'notifcation':notification, 'notification_count':notification_count}

def UpdateNotification(request,pk):
    obj = get_object_or_404(Notification, id=pk)
    obj.is_read = True
    obj.save()
    return redirect('patient')

def createNotification(request):
    user = request.user
    title = "Welcome to Health Sense " + user  
    content = "We are happy to see you here. We are here to help you. You can ask any question related to heart disease. We will try to answer your question as soon as possible."
    is_read = False
    obj = Notification.objects.create(user=user, title=title, content=content, is_read=is_read)
    obj.save()
    return redirect('patient')
    
