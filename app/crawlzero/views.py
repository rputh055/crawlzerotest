from django.shortcuts import render, redirect
from crawlzero.forms import UserForm, FileUploadModelForm
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
import os
from .models import File
from django.core.files.storage import default_storage, FileSystemStorage
from .scrap import Scraper
from .mailing import mail,mailfail
import json
from .scrmail import scrapmail
# from .serializer import FileUploadSerializer

# Create your views here.
# task = Scraper()

def index(request):
    return render(request,'crawlzero/index.html')

@login_required
def special(request):
    return HttpResponse("You are logged in !")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            newuser = authenticate(username=user_form.cleaned_data['username'], password=user_form.cleaned_data['password'])
            login(request, newuser)
            return HttpResponseRedirect(reverse('index'))
        else:
            print(user_form.errors)
    else:
        user_form = UserForm()
    return render(request,'crawlzero/registration.html',
                          {'user_form':user_form,
                           'registered':registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('index'))
            else:
                return HttpResponse("Your account was inactive.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details given")
    else:
        return render(request, 'crawlzero/login.html', {})

@login_required
def upload_file(request):
    if request.method == 'POST':
        upload_file = request.FILES['file']
        fs = FileSystemStorage()
        name = fs.save(upload_file.name, upload_file)
        

        scrapmail.delay(name, request.user.email)
        # infile.delete()
        # response = HttpResponse(outfile, content_type='application/vnd.ms-excel')
        # response['Content-Disposition'] = 'attachment; filename="updated.xls"'
        return HttpResponse("A mail will be sent after processing is done")
        # return response
        # return render(request, 'crawlzero/login.html', {})
    # else:
    #     return HttpResponse('Upload a csv or excel file')
    else:
        form = FileUploadModelForm()
        # serializer = FileUploadSerializer()

        
    # return render(request, 'crawlzero/upload.html', {'form': form})
    return render(request, 'crawlzero/upload.html', {'form': form})