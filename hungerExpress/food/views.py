from django.shortcuts import render
from django.http import HttpResponse
from django.core.validators import EmailValidator
from django.core import exceptions
from . import models

# Create your views here.
def index(request):
    return HttpResponse("Hi! You're here at food app. We are developing!")


def restaurantDisplay(request, zipcode_t):
    header = 'Below is the list of restaurants available in your nearby location'
    restaurant_list = models.Restaurant.objects.filter(zipcode__startswith=zipcode_t[:4])

    context = {
        'header' : header,
        'restaurant_list' : restaurant_list
        }

    return render(request, 'food/restaurantListDisp.html', context)

def menuDisplay(request, restaurant_id_t):
    header = 'Please find below the Menu served by us:'
    menu_list = models.Menu.objects.filter(restaurant_id=restaurant_id_t)
    
    context = {
        'header' : header,
        'menu_item_list' : menu_list,
    }

    return render(request, 'food/menuDisplay.html', context)

def signupform(request):
    return render(request, 'food/signupForm.html',)


def signup(request):
    try:
        f_name = request.POST['f_name']
        l_name = request.POST['l_name']
        email = request.POST['email_id']
        user_name_p = request.POST['user_name']
        password_p = request.POST['password']
        contact_no = request.POST['contact_no']
        address = request.POST['address']
        area = request.POST['area']
        city = request.POST['city']
        state = request.POST['state']
        zipcode = request.POST['zipcode']

        #Validate UserName, return error if already exists
        if validateUserName(user_name_p)==False:
            return render(request,'food/signupForm.html',{'error_message':"Username already exists!"})

        #Validate Email
        validator = EmailValidator()
        validator(email)
        
        #Create New user
        new_user = models.UserValidation(user_name=user_name_p, password=password_p,
                    f_name=f_name, l_name=l_name, email_id=email, contact_no=contact_no,
                    address=address, area=area, city=city, state=state)
       
        new_user.save()
        """
        #User Meta
        meta_list = []
        meta_list.append(models.UserMeta(user_id=new_user, metaclass='f_name', metavalue=f_name))
        meta_list.append(models.UserMeta(user_id=new_user, metaclass='l_name', metavalue=l_name))
        meta_list.append(models.UserMeta(user_id=new_user, metaclass='email', metavalue=email))
        meta_list.append(models.UserMeta(user_id=new_user, metaclass='contact_no', metavalue=contact_no))
        meta_list.append(models.UserMeta(user_id=new_user, metaclass='address', metavalue=address))
        meta_list.append(models.UserMeta(user_id=new_user, metaclass='area', metavalue=area))
        meta_list.append(models.UserMeta(user_id=new_user, metaclass='city', metavalue=city))
        meta_list.append(models.UserMeta(user_id=new_user, metaclass='zipcode', metavalue=zipcode))
        """
    except exceptions.ValidationError as e:
        errmsg,code,whitelist = e.args
        return render(request,'food/signupForm.html',{'error_message':errmsg}) 
    except Exception as e:
        #return HttpResponse("Error! %s (%s)"%(e.message, type(e)))
        return HttpResponse(e)
    string = "Success %s %s"%(user_name_p, password_p)
    return HttpResponse(string)

def validateUserName(user_name):
    try:
        q = models.UserValidation.objects.get(user_name=user_name)
        return False
    except models.UserValidation.DoesNotExist:
        return True
