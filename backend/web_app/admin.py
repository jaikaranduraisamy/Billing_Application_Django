from django.contrib import admin
from .models import *

#Table registration for the Django-Admin page
admin.site.register(tblCustomer)
admin.site.register(tblOrder)
admin.site.register(tblProduct)