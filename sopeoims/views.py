
from django import forms
from django.http import JsonResponse
from .models import InventoryItem
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Sum
from .forms import InventoryItemForm
from .forms import InventoryItemForm, InventoryItemEditForm

class InventoryListCreateView(View):
    def get(self, request):
        form = InventoryItemForm()
        return render(request, 'inventory_form.html', {'form': form})
    
    def post(self, request):
        form = InventoryItemForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.ISellingprice <= 0 or instance.ICost <= 0 or instance.IQuantity <= 0:
                form.add_error(None, 'Invalid Input: Selling price, cost, and quantity must be greater than 0.')
                return render(request, 'inventory_form.html', {'form': form})
            
            if instance.ISellingprice < instance.ICost:
                form.add_error('ISellingprice', 'Selling price cannot be less than the cost price.')
                form.fields['ISellingprice'].widget.attrs.update({'class': 'error'})
                return render(request, 'inventory_form.html', {'form': form})
            if instance.IQuantitysold is not None and instance.IQuantity is not None:
                if instance.IQuantitysold > instance.IQuantity:
                    form.add_error('IQuantitysold', 'Quantity sold must be less than or equal to the available quantity.')
                    form.fields['IQuantitysold'].widget.attrs.update({'class': 'error'})
                    return render(request, 'inventory_form.html', {'form': form})
            if instance.ISellingprice is not None and instance.ICost is not None and instance.IQuantitysold is not None:
                instance.IProfit = (instance.ISellingprice - instance.ICost) * instance.IQuantitysold    
                instance.Revenue = instance.IQuantitysold * instance.ISellingprice

            instance.save()

            return redirect('all_items')
    def show(self, request):
            

        return render(request, 'inventory_form.html', {'form': forms})


def success_view(request):
    return render(request, 'success.html')
def index_view(request):
    return render(request, 'index.html')


def homepage(request):
    items = InventoryItem.objects.all()  
    total_profit, total_revenue, total_items = get_total_profit_and_revenue()
    highest_cost_item = get_highest_cost_item()
    most_sold_item= get_most_sold_items()

    context = {
        'items': items,
        'total_profit': total_profit,
        'total_revenue': total_revenue,
        'total_items': total_items,
        'highest_cost_item': highest_cost_item,
        'most_sold_item': most_sold_item
        
    }

    return render(request, 'Homepage.html', context)

def get_total_profit_and_revenue():
    total_profit = InventoryItem.objects.aggregate(total_profit=Sum('IProfit'))['total_profit']
    total_revenue = InventoryItem.objects.aggregate(total_revenue=Sum('Revenue'))['total_revenue']
    total_items = InventoryItem.objects.count()
    return total_profit or 0, total_revenue or 0, total_items

def get_highest_cost_item():
    highest_cost_item = InventoryItem.objects.order_by('-ICost').first()
    return highest_cost_item

def get_most_sold_items():
    most_sold_items = InventoryItem.objects.order_by('-IQuantitysold').first()  # Change the number as needed
    return most_sold_items

def display_all_items(request):
    items = InventoryItem.objects.all()
    return render(request, 'all_items.html', {'items': items})
def display_all_sell(request):
    items = InventoryItem.objects.all()
    return render(request, 'Sell_Singal.html', {'items': items})



class EditInventoryItemView(View):
    def get(self, request, iin):
        inventory_item = InventoryItem.objects.get(IIN=iin)
        form = InventoryItemEditForm(instance=inventory_item)
        return render(request, 'inventory_edit.html', {'form': form, 'inventory_item': inventory_item})

    def post(self, request, iin):
        inventory_item = InventoryItem.objects.get(IIN=iin)
        form = InventoryItemEditForm(request.POST, instance=inventory_item)
        if form.is_valid():
            instance = form.save(commit=False)
            if instance.ISellingprice <= 0 or instance.ICost <= 0 or instance.IQuantity <= 0:
                form.add_error(None, 'Invalid Input: Selling price, cost, and quantity must be greater than 0.')
                return render(request, 'inventory_form.html', {'form': form})
            if instance.ICost > instance.ISellingprice:
                form.add_error('ISellingprice', 'Selling Price should be greater than or equal to Cost Price.')
                return render(request, 'inventory_edit.html', {'form': form, 'inventory_item': inventory_item})
            if instance.ICost <= instance.ISellingprice:    
                instance.IProfit = instance.calculate_profit()
                instance.Revenue = instance.calculate_revenue()
                instance.save()
                return redirect('all_items')  
        return render(request, 'inventory_edit.html', {'form': form, 'inventory_item': inventory_item})
    
#-------------------------------------------------------------------------------------------------

from .forms import InventoryItemSellForm

class SellItemView(View):
    def get(self, request, iin):
        try:
            inventory_item = InventoryItem.objects.get(IIN=iin)
        except InventoryItem.DoesNotExist:
            return redirect('sale_singal') 

        form = InventoryItemSellForm(instance=inventory_item)
        return render(request, 'sell_item.html', {'form': form, 'inventory_item': inventory_item})

    def post(self, request, iin):
        try:
            inventory_item = InventoryItem.objects.get(IIN=iin)
        except InventoryItem.DoesNotExist:
            return redirect('sale_singal')  

        form = InventoryItemSellForm(request.POST, instance=inventory_item)
        if form.is_valid():
            sold_quantity = form.cleaned_data['IQuantitysold']
            if sold_quantity <= inventory_item.IQuantity: 
                profit = inventory_item.calculate_profit()
                revenue = inventory_item.calculate_revenue()
                inventory_item.IQuantity -= sold_quantity  
                inventory_item.IProfit += profit
                inventory_item.Revenue += revenue
                # Update the inventory quantity
                inventory_item.save()  # Save the updated inventory item to the database
                return redirect('sale_singal')  
            else:
                form.add_error('IQuantitysold', 'Sold quantity exceeds available quantity.')  

        return render(request, 'sell_item.html', {'form': form, 'inventory_item': inventory_item})

#-----------------------==============================================================================================
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import InventoryItem
from .forms import BuyForm

class BuyItemView(View):
    def get(self, request, iin):
        try:
            inventory_item = InventoryItem.objects.get(IIN=iin)
        except InventoryItem.DoesNotExist:
            return redirect('all_items')
        form = BuyForm(instance=inventory_item)
        return render(request, 'buy_item.html', {'form': form, 'inventory_item': inventory_item})

    def post(self, request, iin):
        try:
            inventory_item = InventoryItem.objects.get(IIN=iin)
        except InventoryItem.DoesNotExist:
            return JsonResponse({'error': 'Item not found'}, status=404)

        form = BuyForm(request.POST, instance=inventory_item)
        if form.is_valid():
            bought_quantity = form.cleaned_data['Order']
            if bought_quantity <= 0:
                return JsonResponse({'error': 'Invalid Input'}, status=400)
            InventoryItem.objects.filter(IIN=iin).update(Order=F('Order') + bought_quantity)    
            inventory_item.save()

            return JsonResponse({'message': 'Item added to cart'}, status=200)
        else:
            return JsonResponse({'error': 'Form validation failed'}, status=400)


#==========================Delete=====================

# views.py
from django.shortcuts import render, redirect
from django.views import View
from .models import InventoryItem

class DeleteItemView(View):
    def get(self, request, iin):
        try:
            inventory_item = InventoryItem.objects.get(IIN=iin)
        except InventoryItem.DoesNotExist:
            return redirect('all_items') 

        return render(request, 'delete_items.html', {'inventory_item': inventory_item})

    def post(self, request, iin):
        try:
            inventory_item = InventoryItem.objects.get(IIN=iin)
        except InventoryItem.DoesNotExist:
            return redirect('all_items')  

        inventory_item.delete()  
        return redirect('all_items')  

from django.shortcuts import render, redirect
from .models import InventoryItem
from .forms import InventoryItemForm
from django.db.models import F

def item_soldout(request):
    sold_out_items = InventoryItem.objects.filter(IQuantity__exact=0).exclude(IQuantity__gt=0)

    return render(request, 'sold_out_items.html', {'sold_out_items': sold_out_items})


#================================================list if Transactions==================================================

from django.shortcuts import render
from .models import Received_Transaction

def order_received_view(request):
    items = Received_Transaction.objects.exclude(Order__isnull=True).exclude(Order=0)
    return render(request, 'order_received.html', {'items': items})

from django.shortcuts import render
from .models import Canceled_Transaction

def order_canceled_view(request):
    items = Canceled_Transaction.objects.exclude(Order__isnull=True).exclude(Order=0)
    return render(request, 'not_received_list.html', {'items': items})


#=======================================================================


from django.shortcuts import render, redirect
from django.views.generic import View
from datetime import datetime
from .forms import OrderForm
from .models import InventoryItem, Transaction
from django.http import HttpResponse
'''
class OrderPlacedView(View):
    template_name = 'order_placed.html'
    
    def get(self, request):
        form = OrderForm()
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = OrderForm(request.POST)
        if form.is_valid():
            iquantity = form.cleaned_data['Order']
            
            try:
                item = InventoryItem.objects.get(IIN=iin)
                
                if item.IQuantity >= iquantity:
                    # Check if transaction already exists
                    transaction, created = Transaction.objects.get_or_create(
                        IIN=iin,
                        defaults={
                            'IName': item.IName,
                            'ICost': item.ICost,
                            'Order': iquantity,
                            'Date': datetime.now(),
                            'Status': 'Pending'
                        }
                    )
                    
                    if not created:
                        transaction.ICost = item.ICost
                        transaction.Order += iquantity
                        transaction.Date = datetime.now()
                        transaction.Status = 'Pending'
                        transaction.save()
                    
                    item.IQuantity -= iquantity
                    item.Order = iquantity
                    item.save()
                else:
                    # Handle insufficient quantity error
                    pass
            except InventoryItem.DoesNotExist:
                # Handle item not found error
                pass
        
        return redirect('order_placed')   order_placed_items'''




# views.py
class OrderPlacedView(View):
    template_name = 'order_placed_items.html'
    
    
    def get(self, request, iin):
        try:
            Inventory_Item = InventoryItem.objects.get(IIN=iin)
        except Transaction.DoesNotExist:
            pass
        form = OrderForm()
        context = {
            'Inventory_Item': Inventory_Item,
            'form': form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, iin):
        form = OrderForm(request.POST)
        if form.is_valid():
            Order = form.cleaned_data['Order']
            if Order <= 0:
                return JsonResponse({'error': 'Invalid Input'}, status=400)
          
            try:
                item = InventoryItem.objects.get(IIN=iin)

                if Order <= item.Order:
                    transaction, created = Transaction.objects.get_or_create(
                        IName=item.IName,
                        defaults={
                            'ICost': item.ICost,
                            'Order': Order,
                            'Date': datetime.now(),
                            'Status': 'Pending',
                            'IIN': iin  
                        }
                    )

                    if not created:
                        transaction.ICost = item.ICost
                        transaction.Order = Order
                        transaction.Date = datetime.now()
                        transaction.Status = 'Pending'
                        transaction.save()

                    item.Order = Order
                    item.save()
                else:
                    return JsonResponse({'error': 'Invalid Input!'}, status=400)
            except InventoryItem.DoesNotExist:
                pass
        
        return redirect('update_order', iin=iin)


'''from django.shortcuts import render, redirect
from django.views.generic import View
from .forms import OrderForm  # Import your OrderForm
from .models import InventoryItem, Transaction
from django.http import JsonResponse

class OrderPlacedView(View):
    template_name = 'order_placed_items.html'
    
    def get(self, request, iin):
        try:
            inventory_item = InventoryItem.objects.get(IIN=iin)
        except InventoryItem.DoesNotExist:
            # Handle the case where the inventory item doesn't exist
            # You can redirect or display an error message, for example
            pass
        form = OrderForm()
        context = {
            'inventory_item': inventory_item,
            'form': form,
        }
        return render(request, self.template_name, context)
    
    def post(self, request, iin):
        form = OrderForm(request.POST)
        if form.is_valid():
            order_quantity = form.cleaned_data['Order']
          
            try:
                item = InventoryItem.objects.get(IIN=iin)

                if order_quantity <= item.IQuantity:
                    transaction, created = Transaction.objects.get_or_create(
                        IName=item.IName,
                        defaults={
                            'ICost': item.ICost,
                            'Order': order_quantity,
                            'Date': datetime.now(),
                            'Status': 'Pending',
                            'IIN': iin  
                        }
                    )

                    if not created:
                        transaction.ICost = item.ICost
                        transaction.Order += order_quantity
                        transaction.Date = datetime.now()
                        transaction.Status = 'Pending'
                        transaction.save()

                    item.IQuantity -= order_quantity
                    item.save()
                else:
                    return JsonResponse({'error': 'Order Quantity is Greater than Available Quantity'}, status=400)
            except InventoryItem.DoesNotExist:
                pass
        
        return redirect('update_order', iin=iin)
'''




from django.views import View
from django.shortcuts import redirect
from django.http import HttpResponse
from datetime import datetime
from .models import Transaction, InventoryItem 

class MarkOrderReceivedView(View):
    def post(self, request, *args, **kwargs):
        transaction_id = request.POST.get('transaction_id')
        
        try:
            transaction = Transaction.objects.get(id=transaction_id)
            if transaction.Status == 'Received':
                 return redirect('update_order', iin=transaction.IIN)
            if transaction.Status == 'Cancel':
                return redirect('update_order', iin=transaction.IIN)
            transaction.Status = 'Received'
            transaction.Date = datetime.now()
            transaction.save()

            try:
                item = InventoryItem.objects.get(IName=transaction.IName)

                transaction.ICost = item.ICost
                transaction.Order = item.Order
                transaction.save()

                # Update item quantity
                item.IQuantity = item.Order + item.IQuantity
                item.save()

            except InventoryItem.DoesNotExist:
                return HttpResponse("Associated InventoryItem not found", status=404)

        except Transaction.DoesNotExist:
            return HttpResponse("Transaction not found", status=404)
        
        return redirect('transaction_list')  


class MarkOrderNotReceivedView(View):
    def post(self, request, *args, **kwargs):
        transaction_id = request.POST.get('transaction_id')
        try:
            transaction = Transaction.objects.get(id=transaction_id)
            if transaction.Status == 'Received':
                 return redirect('update_order', iin=transaction.IIN)
            if transaction.Status == 'Cancel':
                return redirect('update_order', iin=transaction.IIN)
            transaction.Status = 'Cancel'
            transaction.Date = datetime.now()
            item = InventoryItem.objects.get(IName=transaction.IName)
            
            transaction.ICost = item.ICost
            transaction.Order = item.Order

            transaction.save()
            item.IQuantitySold = 0
            item.save()

        except Transaction.DoesNotExist:
            pass
        
        return redirect('transaction_list')


from django.shortcuts import render
from .models import Transaction

def transaction_list(request):
    transactions = Transaction.objects.all().order_by('Date')  
    return render(request, 'transaction_list.html', {'transactions': transactions})




from django.shortcuts import render
from django.views.generic import View
from .models import Transaction

class UpdateOrderView(View):
    template_name = 'update_order.html'
    
    def get(self, request, iin):
        transactions = Transaction.objects.filter(IIN=iin)
        return render(request, 'update_order.html', {'transactions': transactions})


class TransactionListView(View):
    template_name = 'order_placedshow.html'  
    def get(self, request):
        transactions = Transaction.objects.all().order_by('Date') 
        return render(request, self.template_name, {'transactions': transactions})


#==============================================management view=======================================
'''from django.conf import settings
import json
from django.shortcuts import render
import os

managementjson = os.path.join(settings.MEDIA_ROOT, 'IMS', 'media', 'management.json')


def management(request):
    try:
        with open(managementjson) as f:
            data = json.load(f)
    except:
        data = {}

    jsonData = json.dumps(data)
    context = {"jsonData": jsonData} 
    context.update(data)

    return render(request, 'management.html', context)'''

def management(request):
    items = InventoryItem.objects.all()  
    return render(request, 'Management.html', {'items': items})  

#=================================Received and canceled=============

