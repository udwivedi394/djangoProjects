from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime

"""
def check_category(value,category_p):
    if value=='None':
        raise ValidationError( _('%(category)s is None. You cannot have subcategory without category'),
                                params = {'value':value},)
"""
"""
def check_category(category_p):
    def innerfn(value):
        if category_p=='None':
            raise ValidationError( _('%(category)s is None. You cannot have subcategory without category'),
                                params = {'value':value},)
        return

    return innerfn
"""
#Validator Class
class CheckCategory:
    def __init__(self,param):
        self.category = param
    
    def __call__(self,value):
        if self.category=='None':
            raise ValidationError( _('%(category)s is None. You cannot have subcategory without category'),
                                params = {'value':value},)
        return 
         

# Create your models here.
class UserValidation(models.Model):
    user_name = models.CharField(max_length=30, unique=True, null=False)
    password = models.CharField(max_length=20, null=False)
    f_name = models.CharField(max_length=20, null=False)
    l_name = models.CharField(max_length=20, null=False)
    email_id = models.CharField(max_length=40, null=False)
    contact_no = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=10, null=True)
    area = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=20, null=True)
    state = models.CharField(max_length=20, null=True)
    zipcode= models.DecimalField(max_digits=6, decimal_places=0)
    def __str__(self):
        return self.user_name

class UserMeta(models.Model):
    user_id = models.ForeignKey(UserValidation, on_delete=models.CASCADE)
    #additional constaint I'll add later at the time of migration
    metaclass = models.CharField(max_length=40)
    metavalue = models.CharField(max_length=200)

class Restaurant(models.Model):
    name = models.CharField(max_length=40, null=False)
    address = models.CharField(max_length=150)
    area = models.CharField(max_length=40, null=False)
    city = models.CharField(max_length=40, null=False)
    zipcode = models.CharField(max_length=6,
                validators=[RegexValidator(regex='^.{6}$',message='Length has to be 6', code='LengthError')])

    contact_no = models.CharField(max_length=20)#, unique=True)

    def __str__(self):
        return self.name

class Menu(models.Model):
    item_id = models.AutoField(primary_key=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=40)
    category = models.CharField(max_length=40, null=True)
    sub_category = models.CharField(max_length=40, null=True)#, validators=[CheckCategory(category)])
    price = models.DecimalField(max_digits=7, decimal_places=2)
    
    def __str__(self):
        return self.item_name

#Order Header: 01-Apr-2018
class OrderHeader(models.Model):
    user = models.ForeignKey(UserValidation, on_delete=models.CASCADE, related_name='header_user_id')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    number_of_items = models.IntegerField(null=True)
    order_value = models.FloatField(null=True)
    taxes = models.FloatField(null=True)
    discount = models.FloatField(null=True)
    net_amount = models.BigIntegerField(null=True)
    order_date = models.DateTimeField(null=True,default=datetime.datetime.now())
    date_created = models.DateTimeField(null=True)
    date_modified = models.DateTimeField(null=True) 
    change_by_user = models.ForeignKey(UserValidation, on_delete=models.CASCADE)

#Order Detail: 01-Apr-2018
class OrderDetail(models.Model):
    order = models.ForeignKey(OrderHeader, on_delete=models.CASCADE)
    user = models.ForeignKey(UserValidation, on_delete=models.CASCADE, related_name='detail_user_id')
    item = models.ForeignKey(Menu, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    base_price = models.DecimalField(max_digits=7, decimal_places=2)
    quantity = models.IntegerField()
    extended_price = models.BigIntegerField()
    order_date = models.DateTimeField()
    date_created = models.DateTimeField(null=True)
    date_modified = models.DateTimeField(null=True)
    change_by_user = models.ForeignKey(UserValidation, on_delete=models.CASCADE, related_name='last_modified_by_user_id')
