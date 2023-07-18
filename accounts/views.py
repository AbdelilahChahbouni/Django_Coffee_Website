from django.shortcuts import render , redirect
from django.contrib import messages
from .models import UserProfile
from django.contrib.auth.models import User
from django.contrib import auth
from allproducts.models import Product
import re




# Create your views here.

def signin(request):
    if request.method == "POST" and "btn-signin" in request.POST:
        
        username = request.POST['username']
        password = request.POST['password']

        new_user = auth.authenticate(username=username , password=password)
        
        if new_user is not None:
            if "rme" not in request.POST:
                request.session.set_expiry(0)
            auth.login(request , new_user)
            #messages.success(request , "You Are Logged in ")
        else:
            messages.error(request , "Your Username or Password Invalid ")

        


        return redirect("signin")
    else:
        return render(request , 'accounts/signin.html')

def logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
    return redirect("index")

def signup(request):
    if request.method == "POST" and "btn-signup" in request.POST:
        # variables for fields
        fname = None
        lname = None
        adress1 = None
        adress2 = None
        state = None
        city = None
        zip_number = None
        username = None
        password = None
        email = None
        checked = None
        is_added = None

        # Get Values From Formes And Check if name in Html is changed
        if "fname" in request.POST: fname = request.POST['fname']
        else: messages.error(request , "Error in fname ")
        if "lname" in request.POST: lname = request.POST['lname']
        else: messages.error(request , "Error in lname ")

        if "address" in request.POST: adress1 = request.POST['address']
        else: messages.error(request , "Error in adress ")

        if "address2" in request.POST: adress2 = request.POST['address2']
        else: messages.error(request , "Error in address2 ")

        if "state" in request.POST: state = request.POST['state']
        else: messages.error(request , "Error in state ")

        if "city" in request.POST: city = request.POST['city']
        else: messages.error(request , "Error in city ")

        if "zip" in request.POST: zip_number = request.POST['zip']
        else: messages.error(request , "Error in zip ")

        if "user" in request.POST: username = request.POST['user']
        else: messages.error(request , "Error in user ")

        if "pass" in request.POST: password = request.POST['pass']
        else: messages.error(request , "Error in pass ")

        if "email" in request.POST: email = request.POST['email']
        else: messages.error(request , "Error in emial ")

        if "term" in request.POST: checked = request.POST['term']
        
        # Check Fields

        if fname and lname and state and city and adress1 and adress2 and username and password and email and zip_number:
            if checked == "on":
                # Check If Username is taken
                if User.objects.filter(username=username).exists():
                    messages.error(request , "This Username Is Taken")
                else:
                    # Check the email is taken
                    if User.objects.filter(email=email).exists():
                        messages.error(request , "This is email is taken")
                    else:
                        # check form of email
                        patt = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
                        if re.match(patt , email):
                            # add user
                            user = User.objects.create_user(first_name=fname , last_name=lname ,email=email , password=password , username=username)
                            user.save()

                            # add userprofile
                            userprofile = UserProfile(user=user , address=adress1 , address2=adress2 , state=state , city=city , zip_number=zip_number)
                            userprofile.save()

                            # clear fields

                            fname = lname = username = password = email = adress1 = adress2 = zip_number = city = state = ""
                            checked = None

                            # add message success
                            messages.success(request , "Your Account is Created ")
                            is_added = True

                        else:
                            messages.error(request , "This is invalid email ")
            else:
                messages.error(request, "You must Agree To Terms ")
        else:
            messages.error(request , "Check Empty Fields ")


        return render(request , 'accounts/signup.html' , {
            'fname':fname,
            'lname':lname,
            'user':username,
            'pass':password,
            'email':email,
            'city':city,
            'address':adress1,
            'address2':adress2,
            'zip':zip_number,
            'state':state,
            'is_added': is_added,

            })
    else:
        return render(request , 'accounts/signup.html')


def profile(request):
    if request.method == "POST" and "btn-profile" in request.POST:
        if request.user is not None and request.user.id != None:
            userprofile = UserProfile.objects.get(user=request.user)
            if request.POST['fname'] and request.POST['lname'] and request.POST['user'] and request.POST['pass'] and request.POST['email'] and request.POST['address'] and request.POST['address2'] and request.POST['city'] and request.POST['state'] and request.POST['zip']:
                request.user.first_name = request.POST['fname']
                request.user.last_name = request.POST['lname']
                #request.user.email = request.POST['email']
                #request.user.username = request.POST['user']
                userprofile.address = request.POST['address']
                userprofile.address2 = request.POST['address2']
                userprofile.city = request.POST['city']
                userprofile.state = request.POST['state']
                userprofile.zip_number = request.POST['zip']
                if not request.POST['pass'].startswith("pbkdf2_sha256"):
                    request.user.set_password(request.POST['pass'])
                request.user.save()
                userprofile.save()
                auth.login(request , request.user)
                messages.success(request, "your data has been saved")
            else:
                messages.error(request , "the values and elements invalid")

        return redirect("profile")
    else:
        if request.user is not None:
            #if request.user.is_anonymous: return redirect("index")
            #if request.user.id == None: return redirect("index")
            context = None
            if not request.user.is_anonymous:
                userprofile = UserProfile.objects.get(user=request.user)
                context = {
                    'fname': request.user.first_name,
                    'lname': request.user.last_name,
                    'user' : request.user.username,
                    'address1': userprofile.address,
                    'address2': userprofile.address2,
                    'state' : userprofile.state,
                    'city' : userprofile.city,
                    'zip' : userprofile.zip_number,
                    'pass' : request.user.password,
                    'email': request.user.email,
                    
                    }
            return render(request , 'accounts/profile.html' , context)


def product_favorite(request , pro_id):
    if request.user.is_authenticated and not request.user.is_anonymous:
        pro_fav = Product.objects.get(pk = pro_id) 
        if Userprofile.objects.filter(user=request.user , product_favorite= pro_fav).exists():
            messages.success(request, "the product already in the list favorite")
        else:
            pass
