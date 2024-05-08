from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.permissions import IsAuthenticated

from rest_framework import mixins 
from rest_framework import generics 
from .serializers import * 
from rest_framework.response import Response
from datetime import datetime

from django.utils.timezone import now
# Create your views here.

class VendorProfileManagment(
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            generics.GenericAPIView
                        ):
    # permission_classes = [IsAuthenticated]
    
    queryset = Vendor.objects.all() 
    serializer_class = VendorProfileProfileManagementSerializer
    
    def post(self, request, *args, **kwargs): 
        return self.create(request,*args,**kwargs)
    
    def get(self,request,*args,**kwargs):
        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs) 
    
    def put(self, request, *args, **kwargs): 
        return self.partial_update(request, *args, **kwargs) 
        
    def delete(self, request, *args, **kwargs): 
        return self.destroy(request, *args, **kwargs) 
    

class PurchaseOrderManagment(
                            mixins.ListModelMixin,
                            mixins.CreateModelMixin,
                            mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            generics.GenericAPIView
):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    
    def post(self,request,*args,**kwargs):
        return self.create(request,*args,**kwargs)
    
    def get (self,request,*args,**kwargs):
        
        vendor = request.query_params.get('vendor_id',None)

        if vendor is not None:
            queryset = self.queryset.filter(vendor=vendor)
            serializer = self.serializer_class(queryset, many=True)  # Serialize the queryset
            return Response(serializer.data)

        if 'pk' in kwargs:
            return self.retrieve(request, *args, **kwargs)
        else:
            return self.list(request, *args, **kwargs)
    
    def put(self, request, *args, **kwargs): 
        
        return self.partial_update(request, *args, **kwargs) 
        
    def delete(self, request, *args, **kwargs): 
        return self.destroy(request, *args, **kwargs) 
    

class AcknowledgePurchaseOrderManagment(mixins.UpdateModelMixin,generics.GenericAPIView):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer

    def put(self, request, *args, **kwargs):
        # Prepare the data with the updated acknowledgment_date
        # data = request.data.copy()
        
        purchase_order = self.get_object()
        current_time = now()
        purchase_order.acknowledgment_date = current_time
        purchase_order.save()
        
        # Proceed with the partial update
        return self.partial_update(request, *args, **kwargs)

        
    

class PerformanceView(mixins.RetrieveModelMixin,generics.GenericAPIView):
    queryset = Vendor.objects.all() 
    serializer_class = PerfomanceMetricsSerializer
    def get(self,request,*args,**kwargs): 
        return self.retrieve(request, *args, **kwargs)