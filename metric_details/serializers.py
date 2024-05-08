from rest_framework import serializers
# from enumchoicefield  import ChoiceEnum, EnumChoiceField
from .models import *

# class Status(ChoiceEnum):
#     pending = "pending"
#     completed = "completed"
#     canceled = "canceled"




class VendorProfileProfileManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = "__all__"

    def create(self, validated_data):
        vendor = Vendor(
            **validated_data
        )
        vendor.save()
        
        return vendor
    

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = "__all__"

    def create(self,validated_data):
        
        purchase_order = PurchaseOrder(
            **validated_data
        )
        purchase_order.save()
        return purchase_order
    

class PerfomanceMetricsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ["on_time_delivery_rate","quality_rating_avg","average_response_time","fulfillment_rate"]
