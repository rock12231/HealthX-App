from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from BaseAPI.models import DataModel
from BaseAPI.serializers import DataSerializer
from django.contrib.auth.models import User
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.
import csv
import os



class DataList(APIView):
     
    # Get all designs
    def get(self, request):
        designs = DataModel.objects.all()
        serializer = DataSerializer(designs, many=True)
        print("Get api called DataList")
        return Response(serializer.data)

    def post(self, request, format=None):
        print(">>>>>>>>>>>",request.data)
        # print user from every request
        # print(">>>>>>>>>>>",request.user)
        # remove user from request.data
        # request.data.pop('user')
        serializer = DataSerializer(data=request.data)
        #  get user in variable from request.data
        current_user = request.data['user']
        csv_file_path = f'BaseAPI/data/{current_user}.csv'
        request.data.pop('user')
        csvdata = [list(request.data.values())]
        
        # check = User.objects.get(username=request.user)
        # print(">>>>>>>>>>>>",check)
        
        if serializer.is_valid():
            serializer.save()
            print(">>>>> Save To DB <<<<<<")
            # Check if the file exists
            if os.path.isfile(csv_file_path):
                # Append data to the existing file
                with open(csv_file_path, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(csvdata)
                print("Successfully appended data to csv file")
            else:
                # Create a new file and write data to it
                with open(csv_file_path, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['cp','trestbps','chol','fbs','restecg','thalach','exang','oldpeak','slope','ca','thal'])
                    writer.writerows(csvdata)
                print("Successfully created csv file and wrote data to it")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("User Not Authenticated")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Design Detail class
class DataDetail(APIView):
    # authentication_class = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]
    
    def get_object(self, pk):
        try:
            return DataModel.objects.get(pk=pk)
        except DataModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(id = pk)
        serializer = DataSerializer(snippet)
        print("Get api called")
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = DataSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print("Put api called")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        print("Delete api called")
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    
    
    # Get design by id
    def get_object(self, id):
        try:
            return DataModel.objects.get(pk=id)
        except DataModel.DoesNotExist:
            raise Http404
        
    # Get API design by id 
    def get(self, id):
        data = self.get_object(id)
        serializer = DataSerializer(data)
        print("Get api called")
        return Response(serializer.data)
    
    # Post API design by id 
    def post(self, request):
        serializer = DataSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        print("Post api called")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # Delete API design by id
    def delete(self, request, id):
        DataModel.objects.all(pk=id).delete()
        print("Delete api called")
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    # Put API design by id
    def put(self, request, id):
        design = DataModel.objects.get(pk=id)
        serializer = DataSerializer(design, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        print("Put api called")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    