from django.shortcuts import render
from django.contrib import messages

# Create your views here.

def signin(request):
    if request.GET:
        messages.info(request , "Testing Message 1 From sigin")
    return render(request , 'accounts/signin.html')



def signup(request):
    if request.GET:
        messages.info(request , "Testing Message 1 From Signup")
    return render(request , 'accounts/signup.html')


def profile(request):
    if request.GET:
        messages.info(request , "Testing Message 1 FRom Profile")
    return render(request , 'accounts/profile.html')
