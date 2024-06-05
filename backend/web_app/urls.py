from django.urls import path
from .views import *

urlpatterns = [
    path('allCustomer', allCustomer, name='allCustomer'),
    path('allProduct', allProduct, name='allProduct'),
    path('allOrder', allOrder, name='allOrder'),
    path('generatePdf', generatePdf, name='generatePdf'),
]

