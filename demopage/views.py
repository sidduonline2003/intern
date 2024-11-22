from django.shortcuts import render,redirect,HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm
from django.contrib.auth import authenticate
import base64
from joblib import load
import cv2
import numpy as np
 
# Create your views here.
def home(request):
    return render(request,'index.html')
 
def login(request):
    if(request.user.is_authenticated):
        return render(request,'login.html')
    if(request.method == "POST"):
        un = request.POST['username']
        pw = request.POST['password']
        #authenticate() is used to check for the values present in the database or not
        #if the values are matched, then it will return the username
        #if the values are not matched, then it will return as 'None'
        # use authenticate(), need to import it from auth package
        user = authenticate(request,username=un,password=pw)
        if(user is not None):
            return redirect('/profile')
        else:
            msg = 'Invalid Username/Password'
            form = AuthenticationForm(request.POST)
            return render(request,'login.html',{'form':form,'msg':msg})
    else:
        form = AuthenticationForm()
        #used to create a basic login page with username and password
        return render(request,'login.html',{'form':form})
 
def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            un = form.cleaned_data.get('username')
            pw = form.cleaned_data.get('password1')
            authenticate(username=un, password=pw)
            return redirect('/login')
        else:
            return render(request, 'register.html', {'form': form})
    else:
        form = UserCreationForm()
        # UserCreationForm() is used to create a basic registration page with username, password, and confirm password
        return render(request, 'register.html', {'form': form})
   
"""def profile(request):
    if(request.method=="POST"):
        if(request.FILES.get('uploadImage')):
            img_name = request.FILES['uploadImage']
            # create a variable for our FileSystem package
            fs = FileSystemStorage()
            filename = fs.save(img_name.name,img_name)
            #urls
            img_url = fs.url(filename)
            return render(request,'profile.html',{'img':img_url})
    else:
        return render(request,'profile.html')"""

"""def profile(request):
    if request.method == "POST":
        if request.FILES.get('uploadImage'):
            img_name = request.FILES['uploadImage'].read()
            encode = base64.b64encode(img_name).decode('utf-8')
            img_url = f"data:image/jpeg;base64,{encode}"
            return render(request, 'profile.html', {'i