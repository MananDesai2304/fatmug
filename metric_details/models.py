from django.db import models

# Create your models here.
class Vendor(models.Model):
    name = models.CharField(max_length=50) 
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50)
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50,unique=True)
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    deilvery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True)


class HistroicalPerfomance(models.Model):
    vendor = models.ForeignKey(Vendor,on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField(null=True)
    quality_rating_avg = models.FloatField(null=True)
    average_response_time = models.FloatField(null=True)
    fulfillment_rate = models.FloatField(null=True)    



