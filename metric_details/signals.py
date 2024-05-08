# from django.contrib.auth.models import User
from .models import *
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import Vendor,HistroicalPerfomance
from datetime import date,datetime
from django.utils.timezone import now
from django.db.models import Q
from django.db.models import Sum
# from django.db.models.functions import DateDiff
@receiver(pre_save,sender=PurchaseOrder)
def test(sender,instance,**kwargs):

    if  instance.id is not None:
        try:
            purchase_order_data = PurchaseOrder.objects.get(pk=instance.id)
        except:
            return None
        
        # GET VENDOR DATA
        vendor_data = Vendor.objects.get(pk=instance.vendor.id)
        current_avrage_response_time = vendor_data.average_response_time
        current_fulfilment_rate = vendor_data.fulfillment_rate

        # GET VENDOR'S PURCHASE ORDER COUNT DETAILS
        vendor_purchase_order = PurchaseOrder.objects.filter(
            vendor = instance.vendor
        )

        vendor_purchase_order_count = vendor_purchase_order.count()

        # print("VENDOR PURCHASE ORDER COUNT",vendor_purchase_order_count)
        vendor_purchase_order_complete_purchase = vendor_purchase_order.filter(
            status = 'completed'
        )
        vendor_purchase_order_complete_purchase_count = vendor_purchase_order_complete_purchase.count(
        )
        
        acknowledged_purchase_order = vendor_purchase_order.filter(
            Q(acknowledgment_date__isnull=False)
        )
        acknowledged_purchase_order_count = acknowledged_purchase_order.count()


        new_acknowledgment_date = instance.acknowledgment_date
        previous_acknowledgment_date = purchase_order_data.acknowledgment_date
        new_status = instance.status
        previous_status = purchase_order_data.status


        if previous_acknowledgment_date != new_acknowledgment_date:
            if acknowledged_purchase_order_count > 0:
                acknowledged_purchase_order_differnce = acknowledged_purchase_order.values_list('issue_date', 'acknowledgment_date')
                
                differences = []
                for date_tuple in acknowledged_purchase_order_differnce:
                    
                    issue_date, acknowledgment_date = date_tuple
                    difference = acknowledgment_date - issue_date
                    differences.append(difference.days)
                total_difference = sum(differences)
                new_difference = total_difference + (purchase_order_data.issue_date - new_acknowledgment_date).days
                updated_response_time_average = new_difference / (acknowledged_purchase_order_count + 1)
            else:
                updated_response_time_average = (purchase_order_data.issue_date - new_acknowledgment_date).days
        else:
            updated_response_time_average = current_avrage_response_time      
        
        

        if previous_status != new_status:
            if new_status == 'completed':
                vendor_purchase_order_complete_purchase_count += 1

            if vendor_purchase_order_complete_purchase_count == 0:
                upadted_fulfilment_rate = current_fulfilment_rate
            else:
                
                upadted_fulfilment_rate = vendor_purchase_order_complete_purchase_count /  (vendor_purchase_order_count )
        
        else:
            upadted_fulfilment_rate = current_fulfilment_rate
        
        vendor_data.average_response_time = updated_response_time_average
        vendor_data.fulfillment_rate = upadted_fulfilment_rate
        
        vendor_data.save()


#
@receiver(post_save,sender=PurchaseOrder)
def update_purchase_order(sender,instance,created,**kwargs):
    vendor_data = Vendor.objects.get(pk=instance.vendor.id)

    # print(vendor_data.po_number)
    if (instance.status.lower() == 'completed'):
        complete_order_queryset = PurchaseOrder.objects.filter(vendor=instance.vendor,status='completed')
        total_complete_order_count = complete_order_queryset.count()
        current_time = now()
        total_complete_rated_order= complete_order_queryset.filter(
            Q(quality_rating__isnull=False)
        )
        total_complete_rated_order_count = total_complete_rated_order.count()

        total_complete_order_before_on_dilvery_date = complete_order_queryset.filter(
            deilvery_date__gte=current_time

        ).count()

        
        
        
        updated_complete_order_before_on_dilever_date =   total_complete_order_before_on_dilvery_date  / total_complete_order_count 
        
        
        
        if instance.quality_rating is not None:
            
            total_rating = total_complete_rated_order.aggregate(total_rating=Sum('quality_rating'))['total_rating']
            upadted_quality_avrage = total_rating / total_complete_rated_order_count

        else:
            upadted_quality_avrage = vendor_data.quality_rating_avg
        
        
        vendor_data.quality_rating_avg = upadted_quality_avrage
        vendor_data.on_time_delivery_rate = updated_complete_order_before_on_dilever_date
        vendor_data.save()  
        new_perfomance_data = HistroicalPerfomance(
            vendor = vendor_data,
            date = datetime.now(),
            on_time_delivery_rate = vendor_data.on_time_delivery_rate,
            quality_rating_avg = vendor_data.quality_rating_avg,
            average_response_time = vendor_data.average_response_time,
            fulfillment_rate = vendor_data.fulfillment_rate
        )
        new_perfomance_data.save()


    
    


        
        
    
