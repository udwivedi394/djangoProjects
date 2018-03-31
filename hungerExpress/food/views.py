from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.validators import EmailValidator
from django.core import exceptions
from django.urls import reverse
from . import models

# Create your views here.
def index(request):
    #return HttpResponse("Hi! You're here at food app. We are developing!")
    return render(request, 'food/index.html',)


def restaurantDisplay(request, username):
    context = {}
    try:
        if request.POST['area_check'] == 'TRUE':
            header = 'Below is the list of restaurants available in your nearby location'
            user = models.UserValidation.objects.get(user_name=username)
            zipcode_t = str(user.zipcode)
            restaurant_list = models.Restaurant.objects.filter(zipcode__startswith=zipcode_t[:4])
            context['location_specific']='True'
        else:
            raise KeyError
    except KeyError:        
        header = "Hi! Check our vast range of restaurant partners"
        restaurant_list = models.Restaurant.objects.all()
    except Exception as e:
        string = "%s %s"%(e,username)
        return HttpResponse(string)
    context.update({
        'header' : header,
        'restaurant_list' : restaurant_list,
        'username' : username,
        })
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
                    address=address, area=area, city=city, state=state, zipcode=zipcode)
        new_user.save()

    except exceptions.ValidationError as e:
        errmsg,code,whitelist = e.args
        return render(request,'food/signupForm.html',{'error_message':errmsg}) 
    except Exception as e:
        return HttpResponse(e)
    string = "Success %s %s"%(user_name_p, password_p)
    return HttpResponseRedirect(reverse('food:RestaurantList', args=(new_user.user_name,)))

def validateUserName(user_name):
    try:
        q = models.UserValidation.objects.get(user_name=user_name)
        return False
    except models.UserValidation.DoesNotExist:
        return True

def loginPage(request):
    return render(request, 'food/login.html', )

def loginValidate(request):
    try:
        username = request.POST['user_name']
        password = request.POST['password']
        
        q = models.UserValidation.objects.get(user_name=username, password=password) 
        return HttpResponseRedirect(reverse('food:RestaurantList', args=(q.user_name,)))   

    
    except models.UserValidation.DoesNotExist:
        e = "Invalid Username/Password"
        return render(request, 'food/login.html', {'error_message':e})
    except Exception as e:
        return render(request, 'food/login.html', {'error_message':e})
