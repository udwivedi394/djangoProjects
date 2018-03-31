from django.urls import path

from . import views

app_name = 'food'

urlpatterns = [
    path('', views.index, name='index'),
    path('loc/<str:username>/', views.restaurantDisplay, name="RestaurantList"),
    path('restaurant/<int:restaurant_id_t>/', views.menuDisplay, name="menu"),
    path('signup/', views.signupform, name="signupform"),
    path('aftersignup/', views.signup, name="signup"),
    path('login/', views.loginPage, name="login"),
    path('loginValidate/', views.loginValidate, name="loginValidate"),
]
