from django.db import models
from django.contrib.auth.models import User
from membership.models import Customer
import datetime
from django.core.validators import MinValueValidator



# Create your models here.
class Inventory(models.Model):
    item_code = models.CharField(max_length=10, unique=True, blank=True)
    item_name = models.CharField(max_length=100, blank=True)
    item_desc = models.CharField(max_length=200, blank=True)
    in_stock = models.IntegerField(validators=[MinValueValidator(0)])
    categories = (
        ('utensils', 'Utensils'),
        ('cookwares', 'Cookwares'),
        ('appliances', 'Appliances'),
        ('dishes', 'Dishes'),
        ('others', 'Others'),
    )
    category = models.CharField(
        max_length=10,
        choices=categories,
        blank= True
    )
    price = models.IntegerField()
    item_image = models.ImageField(null=True, blank=True, upload_to="inventory/")
    stocked_date = models.DateTimeField(auto_now_add=True)
    stocked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    STATUS = (
        ('C', 'Continue'),
        ('D', 'Discontinued'),
    )
    status = models.CharField(
        max_length=1,
        choices=STATUS,
        default='C',
    )

    def __str__(self):
        return self.item_name

    @property
    def get_image_url(self):
        if self.item_image and hasattr(self.item_image, 'url'):
            return self.item_image.url
        else:
            return "http://via.placeholder.com/300x180"


class Offers(models.Model):
    mail_subject = models.CharField(max_length=255)
    mail_body = models.CharField(max_length=255)
    mail_date = models.DateField()
    mailStatus = (
        ('pending', 'Pending'),
        ('sent', 'Sent'),
    )
    mail_status= models.CharField(
        max_length=7,
        choices=mailStatus,
        default='Pending',
    )


class Sales(models.Model):
    total_price = models.IntegerField()
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    discount = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)


class SalesItem(models.Model):
    sales = models.ForeignKey(Sales, on_delete=models.SET_NULL, null=True)
    item = models.ForeignKey(Inventory, on_delete=models.SET_NULL, null=True)
    purchase_unit = models.IntegerField()
    line_total = models.IntegerField()

