from django.urls import path

from . import views

app_name = 'food'

urlpatterns = [
    path('', views.index, name='index'),
    path('loc/<str:zipcode_t>/', views.restaurantDisplay, name="RestaurantList"),
    path('restaurant/<int:restaurant_id_t>/', views.menuDisplay, name="menu"),
    path('signup/', views.signupform, name="signupform"),
    path('aftersignup/', views.signup, name="signup") 
]
