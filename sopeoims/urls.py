from django.urls import path
from . import views
# sopeoims/urls.py
from django.urls import path
from .views import InventoryListCreateView ,index_view, order_received_view ,BuyItemView, homepage,display_all_items,EditInventoryItemView,SellItemView,DeleteItemView,OrderPlacedView,display_all_sell
from django.urls import path
from .views import OrderPlacedView, MarkOrderReceivedView, MarkOrderNotReceivedView
from .views import transaction_list

from django.urls import path
from .views import OrderPlacedView,order_canceled_view, MarkOrderReceivedView, MarkOrderNotReceivedView, UpdateOrderView,TransactionListView

urlpatterns = [
    path('index/', index_view, name='index'),
    path('inventory/', InventoryListCreateView.as_view(), name='create_inventory_item'), 
    path('home/',homepage, name='Home_page'),
    path('inventory/all/', display_all_items, name='all_items'),
    path('inventory/edit/<str:iin>/', EditInventoryItemView.as_view(), name='edit_inventory_item'),
    path('sell/<str:iin>/', SellItemView.as_view(), name='sell_item'),
    path('buy/<int:id>/', BuyItemView.as_view(), name='buy_item1'),
    path('api/buy/<str:iin>/', BuyItemView.as_view(), name='buy_item'),
    path('delete/<str:iin>/', DeleteItemView.as_view(), name='delete_item'),
    path('soldout/', views.item_soldout, name='item_soldout'),
    path('order/', OrderPlacedView.as_view(), name='order_placed'),
    path('order_placed_items/<str:iin>/', OrderPlacedView.as_view(), name='order_placed_items'),
    path('sellsingal/', display_all_sell, name='sale_singal'),
    path('receivedorder/', order_received_view, name='order_received'),
    path('Canceled-order/', order_canceled_view, name='order_canceled'),
    path('update-order/<str:iin>/', UpdateOrderView.as_view(), name='update_order'),

    path('order-placed/', TransactionListView.as_view(), name='order_placedshow'),
    path('mark-received/', MarkOrderReceivedView.as_view(), name='mark_received'),
    path('mark-not-received/', MarkOrderNotReceivedView.as_view(), name='mark_not_received'),
    path('transaction-list/', transaction_list, name='transaction_list'),
    path('mark-received/', MarkOrderReceivedView.as_view(), name='mark_received'),
    path('mark-not-received/', MarkOrderNotReceivedView.as_view(), name='mark_not_received'),
    path('management/', views.management, name='management'),
   
]



from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

