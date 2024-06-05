from django.db import models

# Create your models here.
class tblProduct(models.Model):
    ProductId = models.AutoField(primary_key=True)
    ProductName = models.CharField(max_length=1000, null=False)
    AvailableStock = models.IntegerField(null=False)
    UnitPrice = models.FloatField(null=False)
    TaxPercentage = models.FloatField(null=False)

    class Meta:
        db_table = 'tblProduct'
    
class tblCustomer(models.Model):
    CustomerId = models.AutoField(primary_key=True)
    CustomerEmailId = models.CharField(max_length=1000, null=False)

    class Meta:
        db_table = 'tblCustomer'


class tblOrder(models.Model):
    OrderId = models.AutoField(primary_key=True)
    CustomerId = models.IntegerField(null=False)
    ProductIds = models.CharField(max_length=1000, null=False)
    Quantity = models.CharField(max_length=1000, null=False)
    PaidDenominations = models.CharField(max_length=1000, null=False)
    BalanceDenominations = models.CharField(max_length=1000, null=False)
    TotalAmountPaid = models.FloatField(null=False)
    TotalAmountReturn = models.FloatField(null=False)
    OrderDate = models.DateTimeField(null=False)

    class Meta:
        db_table = 'tblOrder'