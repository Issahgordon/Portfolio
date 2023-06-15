
# Create your views here.
from django.shortcuts import render,redirect
from django.urls import reverse
from . serializers import Manager_Serializer
from . models import SignUp_info,Cookie_Handler,Books
from rest_framework.response import Response
from rest_framework.views import APIView
from pathlib import Path
from django.core.files.storage import FileSystemStorage
import os
from django.db.models import Q
import shutil
from time import *
import uuid
import random
import math
import email, smtplib, ssl
from tkinter import filedialog
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib, ssl
from django.utils.translation import gettext as _
BASE_DIR = Path(__file__).resolve().parent.parent





#================================================ Login =======================================================
class Home(APIView):
    def get(self , request):
      book = Books.objects.all()[0:4]
      last = Books.objects.last()
      if 'csrf-session-xdii-token' in request.COOKIES:
         
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          User_data = SignUp_info.objects.get(id=int(find.User))
          return render(request , "Home/index.html", {"Data":User_data,"Books":book,"Last":last})
         except:
           val = {"id":"None"}
           
           return render(request , "Home/index.html",{"Data":val,"Books":book,"Last":last})
      else:
         val = {"id":"None"}
         
         return render(request , "Home/index.html",{"Data":val,"Books":book,"Last":last})

class About(APIView):
    def get(self , request):
      if 'csrf-session-xdii-token' in request.COOKIES:
         
         
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          User_data = SignUp_info.objects.get(id=int(find.User))
          return render(request , "Home/about.html", {"Data":User_data})
         except:
           val = {"id":"None"}
           
           return render(request , "Home/about.html",{"Data":val})
      else:
         val = {"id":"None"}
         
         return render(request , "Home/about.html",{"Data":val})


class Manager_Login(APIView):
    def get(self , request):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          User_data = SignUp_info.objects.get(id=int(find.User))
          return redirect('home')
         except:
           return render(request , "Home/signup.html")
      else:
         return render(request , "Home/signup.html")
      
    def post(self, request):
       current_time = strftime("%H:%M:%S %p")
       try:    
          data = SignUp_info.objects.get(Email=request.data['Email'], Password=request.data['Password'])  
          response =  redirect('home')
          try:
            look_up = Cookie_Handler.objects.get(User=data.id, Type="Manager")
            generated_uuid = look_up.Cookie
          except:
            generated_uuid = uuid.uuid1()
            Cookie_Handler.objects.create(User=data.id,Cookie = generated_uuid,Type="Manager")
          response.set_cookie('csrf-session-xdii-token',generated_uuid)
          #Notifications.objects.create(Status = "New",Uid = data.id, Type="Manager", Info=f"You have successfully logged in on {current_time}.")
          return response 
       except:
         return render (request, 'Home/error2.html' )
       

class Manager_Logout(APIView):
    def get(self , request):
      response = redirect("home")
      response.delete_cookie('csrf-session-xdii-token')

      return response

#================================================ Login =======================================================




#================================================ Register ===================================================

class Manager_Register(APIView):
   
    def post(self, request):
         try:    
          serializer = Manager_Serializer(data=request.data)
          try:
            get = SignUp_info.objects.get(Email=request.data["Email"])
            return render (request, 'Home/error3.html' )
          except:
            pass

          print(serializer)
          if serializer.is_valid():
             serializer.save()

             complete = SignUp_info.objects.last()
             rand_int =  random.randint(1,10)
             shutil.copyfile(f"{BASE_DIR}/static/Default/{rand_int}.jpg", f"{BASE_DIR}/media/Users/{str(complete.id)}.jpg")
             response =  redirect('home')
             try:
               look_up = Cookie_Handler.objects.get(User=complete.id, Type="Manager")
               generated_uuid = look_up.Cookie
             except:
               generated_uuid = uuid.uuid1()
               Cookie_Handler.objects.create(User=complete.id,Cookie = generated_uuid,Type="Manager")
             response.set_cookie('csrf-session-xdii-token',generated_uuid)
             return response 
          else:
             
            return render (request, 'Home/error1.html' )
         except:
             return render (request, 'Home/error1.html' )


class Dashboard(APIView):
    def get(self , request):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          User_data = SignUp_info.objects.get(id=int(find.User))
          books = Books.objects.filter(User= User_data.id)
          accounts = SignUp_info.objects.all().count()
          all = Books.objects.all()
          trends = 0
          for i in all:
              if int(i.Rate) > 70:
                trends+=1

          context = {"Data":User_data,"Books":books,"My_Books":books.count,"Trends":trends,"Accounts":accounts,"All":all.count()}
          return render(request, "Manager/index.html",context)
         except:
          return redirect("login")
      else:
        return redirect("login")

class Upload(APIView):
    def get(self , request):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          User_data = SignUp_info.objects.get(id=int(find.User))
          books = Books.objects.filter(User= User_data.id)


          context = {"Data":User_data,"Books":books}
          return render(request, "Manager/upload.html",context)
         except:
           return redirect("login")
      else:
         return redirect("login")
    def post(self , request):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          User_data = SignUp_info.objects.get(id=int(find.User))
         # current_date = strftime("%Y-%m-%d")
         # rand = random.randint(0,1000)
          data = request.data
          Books.objects.create(Name=data["Name"],Category=data["Category"],
                                      User=User_data.id,Rate=data["Rate"],About=data["About"]
                                                                         )
          id = Books.objects.last()
          
            
          uploading_file = request.FILES['New_Img']
          fs = FileSystemStorage()
          fs.save("Covers//"+str(id.id)+".jpg",uploading_file) 
          uploading_file = request.FILES['Book']
          fs = FileSystemStorage()
          fs.save("Books//"+str(id.id)+".pdf",uploading_file) 
          return redirect('dashboard')
         except:
             return redirect("login")

      else:
         return redirect('login')


class Delete_Book(APIView):
    def post(self , request):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          User_data = SignUp_info.objects.get(id=int(find.User))
          current_date = strftime("%Y-%m-%d")
          Books.objects.get(User= User_data.id,id=int(request.data["id"])).delete()
          try:
            os.remove(f'{BASE_DIR}/media/Covers/{request.data["id"]}.jpg')
          except:
            pass 
          try:
            os.remove(f'{BASE_DIR}/media/Books/{request.data["id"]}.pdf')
          except:
            pass 
          
          return Response('Ok')
         except:
           return Response('Error')
      else:
         return redirect('Error')
      
class Select_Book(APIView):
    def get(self , request,pk):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          User_data = SignUp_info.objects.get(id=int(find.User))
          book = Books.objects.get(id=pk)


          context = {"Data":User_data,"Book":book}
          return render(request, "Home/single-product.html",context)
         except:
           return redirect("login")
      else:
        return redirect("login")


      
class Categories(APIView):
    def get(self , request):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          User_data = SignUp_info.objects.get(id=int(find.User))
          
          data = ["Action and Adventure","Classics","Fantasy",
                        "Historical Fiction","Horror","Mystery and Thrillers", "Romance",
                        "Science Fiction","Short Stories", "Biographies and Memoirs",
                        "Business","Cookbooks", "Health and Fitness","History",
                        "Self-Help","Travel","Picture Books","Chapter Books","Young Adult"
                  ]
          listed =[]
          for i in data:
            book = Books.objects.filter(Category = i).count()
            listed.append({"Name":i,"Books":book})
          context = {"Data":User_data,"Categories":listed}
          return render(request, "Home/shop.html",context)
         except:
           return redirect("login")
      else:
         return redirect("login")

class Select_Category(APIView):
    def get(self , request,pk):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          User_data = SignUp_info.objects.get(id=int(find.User))
          books = Books.objects.filter(Category=pk)


          context = {"Data":User_data,"Book":books,"Name":pk}
          return render(request, "Home/listed.html",context)
         except:
           return redirect("login")
      else:
        return redirect("login")

class Trends(APIView):
    def get(self , request):
      if 'csrf-session-xdii-token' in request.COOKIES:
         user1_check = request.COOKIES['csrf-session-xdii-token']
         try:
          find = Cookie_Handler.objects.get(Cookie=user1_check)
          User_data = SignUp_info.objects.get(id=int(find.User))
          books = Books.objects.all()
          listed = []
          for i in books:
             if int(i.Rate) > 70:
                listed.append(i)


          context = {"Data":User_data,"Book":listed}
          return render(request, "Home/trends.html",context)
         except:
          return redirect("login")
      else:
        return redirect("login")
