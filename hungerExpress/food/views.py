from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.validators import EmailValidator
from django.core import exceptions
from django.urls import reverse
from . import models
import datetime

GST_RATE = 5
MAX_DISCOUNT = 30000
DISCOUNT_RATE = 15

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

def menuDisplay(request, username, restaurant_id_t):
    header = 'Please find below the Menu served by us:'
    menu_list = models.Menu.objects.filter(restaurant_id=restaurant_id_t)
    
    context = {
        'header' : header,
        'menu_item_list' : menu_list,
        'restaurant_id' : restaurant_id_t,
        'username' : username,
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
        #return render(request, 'food/login.html', {'error_message':e})
        return HttpResponseRedirect(reverse('food:RestaurantList', args=(q.user_name,)))   

def placeOrder(request, restaurant_id_t, username):
    menu_item_ids = list(map(int, request.POST.getlist('menu')))
    menu_item_qtys = list(map(int, request.POST.getlist('qty')))
    menu_item_ext_qtys = list(map(float, request.POST.getlist('extqty')))

    menu_list = models.Menu.objects.filter(restaurant_id=restaurant_id_t)
    user = models.UserValidation.objects.get(user_name=username)
    user_id_t = user.id
    
    if sum(menu_item_qtys)==0:
        context = {
        'header' : 'Please find below the menu served by us!',
        'menu_item_list' : menu_list,
        'restaurant_id' : restaurant_id_t,
        'error_message': 'No item selected!'}
        return render(request,'food/menuDisplay.html',context)
    
    string = "Hi! Order placed" + '<br>'
    string += ' '.join(str(i) for i in menu_item_ids) + '<br>'
    string += ' '.join(str(i) for i in menu_item_qtys) + '<br>'
    string += ' '.join(str(i) for i in menu_item_ext_qtys)

    order_header = models.OrderHeader(user_id=user_id_t, restaurant_id=restaurant_id_t,change_by_user_id=user_id_t)
    order_header.save()

    order_list = []
    order_value = 0
    #place orders
    #try:
    if request:
        for ctr in range(len(menu_item_ids)):
            if menu_item_qtys[ctr] > 0:
                menu_item = menu_list.get(pk=menu_item_ids[ctr])
                new_order = models.OrderDetail(base_price=menu_item.price,
                            quantity=menu_item_qtys[ctr], extended_price=menu_item.price*menu_item_qtys[ctr]*100,
                            order_date=datetime.datetime.now(), change_by_user_id=user_id_t,
                            item_id=menu_item.item_id, order_id=order_header.id, restaurant_id = restaurant_id_t,
                            user_id = user_id_t)
                order_list.append(new_order)
                order_value += menu_item.price*menu_item_qtys[ctr]*100
        tax = (GST_RATE)*order_value
        discount = max(MAX_DISCOUNT,(DISCOUNT_RATE)*order_value)
        net_amount = order_value+tax-discount
        
        order_header.order_value = order_value
        order_header.taxes = tax
        order_header.discount = discount
        order_header.net_amount = net_amount

        order_header.save()
        
        context = { 'header': 'Thank you for using HungerExpress! Your order has been successfully placed.',
                    'order_list':order_list,
                    'order_header':order_header,
                    'menu':menu_list,
                    'username': username}
        return render(request, 'food/orderSummary.html', context)

    #except Exception as e:
    #    return HttpResponse(e)                   
