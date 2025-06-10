from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("app1.urls")),
    path('qrScanner/',include("qrScanner.urls")),
    path('product_list/',include("product_list.urls")),
    path('orders/',include("orders.urls")),
    path('purchases/',include("purchases.urls")),
    path('records/',include("records.urls")),
]
