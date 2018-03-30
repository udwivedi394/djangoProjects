from django.shortcuts import render
from django.http import HttpResponse
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
