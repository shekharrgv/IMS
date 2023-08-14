from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import pre_save
from django.dispatch import receiver

class User(AbstractUser):
    # Add custom fields or behaviors if needed.
    pass
# models.py
from django.db import models

class InventoryItem(models.Model):
    IName = models.CharField(max_length=7)
    ICost = models.IntegerField()
    IQuantity = models.IntegerField()
    ISellingprice = models.IntegerField()
    IQuantitysold = models.IntegerField(default=0)
    IProfit = models.IntegerField(null=True, blank=True)
    Revenue = models.IntegerField(null=True, blank=True)
    IIN = models.CharField(max_length=7, unique=True, blank=True)
    Order = models.IntegerField(null=True)

    def savesell(self, *args, **kwargs):
        if self.IQuantitysold > 0:
            self.IQuantity = self.IQuantity - self.IQuantitysold
        super().save(*args, **kwargs)


    def __str__(self):
        return self.IName

    def save_withiin(self, *args, **kwargs):
        if not self.IIN:
            latest_item = InventoryItem.objects.order_by('-id').first()
            if latest_item:
                latest_iin = latest_item.IIN[4:]
                try:
                    latest_iin = int(latest_iin)
                except ValueError:
                    latest_iin = 0
            else:
                latest_iin = 0

            next_iin_number = latest_iin + 1
            self.IIN = f"ITEM{next_iin_number:03}"

        super(InventoryItem, self).save(*args, **kwargs)

    def calculate_profit(self):
        return (self.ISellingprice - self.ICost) * self.IQuantitysold

    def calculate_revenue(self):
        return self.IQuantitysold * self.ISellingprice
    def delete(self, *args, **kwargs):
        Transaction.objects.filter(IIN=self.IIN).delete()
        super().delete(*args, **kwargs)
@receiver(pre_save, sender=InventoryItem)
def generate_iin(sender, instance, **kwargs):
    if not instance.IIN:
        latest_item = InventoryItem.objects.order_by('-id').first()
        if latest_item:
            latest_iin = latest_item.IIN[4:]
            try:
                latest_iin = int(latest_iin)
            except ValueError:
                latest_iin = 0
        else:
            latest_iin = 0

        next_iin_number = latest_iin + 1
        instance.IIN = f"ITEM{next_iin_number:03}"     


class Transaction(models.Model):
    IIN = models.CharField(max_length=7, unique=True, blank=True)
    IName = models.CharField(max_length=255)
    ICost = models.IntegerField()
    Order = models.IntegerField()
    Date = models.DateTimeField()
    Status = models.CharField(max_length=50)
    def __str__(self):
        return self.IName
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.Status == 'Received':
            received_transaction, _ = Received_Transaction.objects.get_or_create(
                IIN=self.IIN,
                IName=self.IName,
                ICost=self.ICost,
                Order=self.Order,
                Date=self.Date,
                Status=self.Status
            )
        
        elif self.Status == 'Cancel':
            canceled_transaction, _ = Canceled_Transaction.objects.get_or_create(
                IIN=self.IIN,
                IName=self.IName,
                ICost=self.ICost,
                Order=self.Order,
                Date=self.Date,
                Status=self.Status
            )
          

    
class Received_Transaction(models.Model):
    IIN = models.CharField(max_length=7, blank=True)
    IName = models.CharField(max_length=255)
    ICost = models.IntegerField()
    Order = models.IntegerField()
    Date = models.DateTimeField()
    Status = models.CharField(max_length=50)
    def __str__(self):
        return self.IName
class Canceled_Transaction(models.Model):
    IIN = models.CharField(max_length=7, blank=True)
    IName = models.CharField(max_length=255)
    ICost = models.IntegerField()
    Order = models.IntegerField()
    Date = models.DateTimeField()
    Status = models.CharField(max_length=50)
    def __str__(self):
        return self.IName
  
    
class All_Transaction(models.Model):
    IIN = models.CharField(max_length=7, unique=True, blank=True)
    IName = models.CharField(max_length=255)
    ICost = models.IntegerField()
    Order = models.IntegerField()
    Date = models.DateTimeField()
    Status = models.CharField(max_length=50)
    def __str__(self):
        return self.IName

from django.db import models

class NotReceived(models.Model):
    IName = models.CharField(max_length=7)
    ICost = models.IntegerField()
    IQuantity = models.IntegerField()
    ISellingprice = models.IntegerField()
    IQuantitysold = models.IntegerField(default=0)
    IProfit = models.IntegerField(null=True, blank=True)
    Revenue = models.IntegerField(null=True, blank=True)
    Status = models.CharField(max_length=7)
    IIN = models.CharField(max_length=7)

    def __str__(self):
        return self.IName

    def save(self, *args, **kwargs):
        if not self.IIN:
            inventory_item = InventoryItem.objects.filter(IName=self.IName).first()
            if inventory_item:
                self.IIN = inventory_item.IIN

        super().save(*args, **kwargs)



# models.py
from django.db import models

class OrderItem(models.Model):
    IName = models.CharField(max_length=10)
    ICost = models.DecimalField(decimal_places=2, default=0.0, max_digits=10)
    IQuantitysold = models.PositiveIntegerField()
    received = models.BooleanField(default=False)
    not_received = models.BooleanField(default=False)
    order = models.ForeignKey('Order', on_delete=models.CASCADE)

    def __str__(self):
        return self.IName



class Order(models.Model):
    IQuantity = models.PositiveIntegerField()

    def __str__(self):
        return f"Order ID: {self.id}"

