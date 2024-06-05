from django.shortcuts import render
from .models import *
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
import datetime
from django.template.loader import get_template
from xhtml2pdf import pisa


""" *********** POST: allCustomer *************

This function is used to get all the customers from the tblCustomer

*************** RETURN: Json data of customers ************* """
@csrf_exempt
def allCustomer(request):
    try:
        temp={"Data":{"customers":[]}}
        data = temp['Data']
        customerData = data['customers']
        customers = tblCustomer.objects.all()
        for customer in customers:
            jsonData = {
                "customerId":customer.CustomerId,
                "customerEmailId":customer.CustomerEmailId
            }
            customerData.append(jsonData)
        return JsonResponse({"Data":temp['Data'],"Status":0,"Message":200})
    except:
        return JsonResponse({"Data":[],"Status":1,"Message": 500})


""" *********** POST: allProduct *************

This function is used to get all the products from the tblProduct

*************** RETURN: Json data of products ************* """
@csrf_exempt
def allProduct(request):
    try:
        temp={"Data":{"products":[]}}
        data = temp['Data']
        productData = data['products']
        products = tblProduct.objects.all()
        for product in products:
            jsonData = {
                "ProductId":product.ProductId,
                "ProductName":product.ProductName,
                "AvailableStock":product.AvailableStock,
                "UnitPrice":product.UnitPrice,
                "TaxPercentage":product.TaxPercentage
            }
            productData.append(jsonData)
        return JsonResponse({"Data":temp['Data'],"Status":0,"Message":200})
    except:
        return JsonResponse({"Data":[],"Status":1,"Message": 500})


""" *********** POST: allOrder *************

This function is used to get all the orders from the tblOrder

*************** RETURN: Json data of orders ************* """
@csrf_exempt
def allOrder(request):
    try:
        temp={"Data":{"orders":[]}}
        data = temp['Data']
        orderData = data['orders']
        orders = tblOrder.objects.all()
        for order in orders:
            jsonData = {
                "OrderId":order.OrderId,
                "CustomerId":order.CustomerId,
                "ProductIds":order.ProductIds,
                "Quantity":order.Quantity,
                "PaidDenominations":order.PaidDenominations,
                "BalanceDenominations":order.BalanceDenominations,
                "TotalAmountPaid":order.TotalAmountPaid,
                "TotalAmountReturn":order.TotalAmountReturn,
                "OrderDate":order.OrderDate
            }
            orderData.append(jsonData)
        return JsonResponse({"Data":temp['Data'],"Status":0,"Message":200})
    except:
        return JsonResponse({"Data":[],"Status":1,"Message": 500})


""" *********** POST: generatePdf *************

This function gets the json data as request and perform the following operations
1) Create new user if user is not present in database.
2) Create a new order details for the curresponding user.
3) Generate the order bill as pdf.

*************** RETURN: pdf data ************* """
@csrf_exempt
def generatePdf(request):
    try:
      context = json.loads(request.body)
      errorMessage = ""
      
      customerEmailId = context["customerEmail"]
      totalAmount = context["totalAmount"]
      
      hasCustomer = tblCustomer.objects.filter(CustomerEmailId = customerEmailId)
      if hasCustomer:
        customerId = hasCustomer[0].CustomerId
      else:
        newCustomer = tblCustomer()
        newCustomer.CustomerEmailId = customerEmailId
        newCustomer.save()
        customerId = newCustomer.CustomerId
      
      productList = context["billSection"]
      productArray = []
      quantityArray = []
      billAmount = 0
      for product in productList:
        productDetails = tblProduct.objects.filter(ProductId = int(product['product_Id']))
        if productDetails:
            billAmount += (productDetails[0].UnitPrice * int(product['quantity']))
            productArray.append(product['product_Id'])
        else:
            templatePath = 'templates/error.html'
            errorMessage = "Product Not Found"
            break
              
        quantityArray.append(product['quantity'])

      context['billAmount'] = billAmount
      context['billTotalTax'] = (billAmount*8)/100
      context['billNetPrice'] = billAmount + ((billAmount*8)/100)
      context['billRoundPrice'] = round(billAmount + ((billAmount*8)/100))
      context['billBalanceAmount'] = totalAmount - round(billAmount + ((billAmount*8)/100))
      
      if context['billBalanceAmount'] < 0:
        errorMessage = "Customer Need to pay money " + str(context['billBalanceAmount'] * -1)
      
      denominationList = context["denominations"]
      amountArray = []
      countArray = []
      for denominations in denominationList:
          number = int(denominations.replace("rupee", ""))
          amountArray.append(number)
          countArray.append(int(denominationList[denominations]))
      
      returnDenominations = calculate_change(amountArray, countArray, billAmount+((billAmount*8)/100))
      context['returnDenominations'] = returnDenominations
      
      if returnDenominations == None:
        errorMessage = "The customer has not provided enough money to cover the bill."
      
      if errorMessage == "":
        templatePath = 'templates/billingTemplate.html'
        filePath = os.path.join(os.path.dirname(__file__), templatePath)
        template = get_template(filePath)
        html = template.render(context)
      else:
        templatePath = 'templates/error.html'
        filePath = os.path.join(os.path.dirname(__file__), templatePath)
        template = get_template(filePath)
        html = template.render({"errorMessage": errorMessage})

      response = HttpResponse(content_type='application/pdf')
      response['Content-Disposition'] = 'filename="Billing_report"'
      
      pisaStatus = pisa.CreatePDF(html, dest=response)
  
      if not pisaStatus.err:
        context["customerId"] = customerId
        context["productArray"] = productArray
        context["quantityArray"] = quantityArray
        saveStatus = saveOrder(context)
        if saveStatus == None:
          return response
        else:
          return JsonResponse({'error': "Error in saving order"}, status=500)
    except:
      return JsonResponse({'error': str(e)}, status=500)


""" *********** Function: calculate_change *************

This function is used return amount needed to send back to customer
@param1: currency value List
@param2: currency count List
@param3: total bill amount Integer

*************** RETURN: dictionary array ************* """
def calculate_change(currency_values, customer_notes, total_bill):
    total_paid = sum(value * count for value, count in zip(currency_values, customer_notes))
    change_to_return = total_paid - total_bill
    
    if change_to_return < 0:
        return []
    
    change_distribution = {}
    remaining_change = change_to_return
    
    for value in sorted(currency_values, reverse=True):
        if remaining_change <= 0:
            break
        max_notes = remaining_change // value
        if max_notes > 0:
            #change_distribution.append((value, int(max_notes)))
            change_distribution[value] = str(int(max_notes))
            remaining_change -= value * max_notes
    
    if remaining_change > 0:
        return []
    
    return [change_distribution]


""" *********** POST: saveOrder *************

This function is used save the order details into the database.

*************** RETURN: string ************* """
def saveOrder(data):
    try:
      newOrder = tblOrder()
      newOrder.CustomerId = data["customerId"]
      newOrder.ProductIds = data["quantityArray"]
      newOrder.Quantity = data["productArray"]
      newOrder.PaidDenominations = data["denominations"]
      newOrder.BalanceDenominations = data["returnDenominations"]
      newOrder.TotalAmountPaid = data["totalAmount"]
      newOrder.TotalAmountReturn = data["billBalanceAmount"]
      newOrder.OrderDate = datetime.date.today()
      newOrder.save()
      return None
      
    except json.JSONDecodeError:
      return "Error is saving order."
    except Exception as e:
      return str(e)
