from django.urls import path,include
from .views import *
# from rest_framework.authtoken.views import obtain_auth_token
urlpatterns = [
    # path('api-token-auth/', obtain_auth_token, name='api_token_auth'),
    path('vendors', VendorProfileManagment.as_view()),
    path('vendors/<int:pk>', VendorProfileManagment.as_view()),
    path('purchase_orders',PurchaseOrderManagment.as_view()),
    path('purchase_orders/<int:pk>', PurchaseOrderManagment.as_view()),
    path('purchase_orders/<int:pk>/acknowledge',AcknowledgePurchaseOrderManagment.as_view()),
    path('vendors/<int:pk>/performance',PerformanceView.as_view())
]


# https://www.phind.com/search?cache=unz1jpo1tdhkmt9iuylqqps1