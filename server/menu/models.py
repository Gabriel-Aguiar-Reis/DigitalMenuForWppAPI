import uuid

from django.db import models

class ShopConfig(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    shop_name = models.CharField(max_length=255)
    opening_hours = models.JSONField(default=list, blank=True, null=True)
    theme = models.JSONField(default=list, blank=True, null=True)
    
    def __str__(self):
        return f'<{self.shop_name}> {self.id}'

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    ingredients = models.JSONField(default=list, blank=True, null=True)
    size = models.CharField(max_length=20, blank=True, null=True)
    type = models.ForeignKey('Type', on_delete=models.CASCADE, blank=True, null=True, related_name='products')
    promotion = models.ForeignKey('Campaign', on_delete=models.CASCADE, blank=True, null=True, related_name='products')
    percentual_margin = models.DecimalField(max_digits=4, decimal_places=3, default=0)
    cost_price = models.DecimalField(max_digits=6, decimal_places=2, default=0, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0, blank=True)
    post_discount_price = models.DecimalField(max_digits=6, decimal_places=2, default=0, blank=True)
    units = models.IntegerField(default=0)
    in_stock = models.BooleanField(default=True)
    
    def __str__(self):
        return f'<{self.type.name}> {self.name}'

class Type(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    promotion = models.ForeignKey('Campaign', on_delete=models.CASCADE, blank=True, null=True)
    percentual_margin = models.DecimalField(max_digits=4, decimal_places=3, default=0)
    
    def __str__(self):
        return f'{self.name}'

class Campaign(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    expiration_date = models.DateTimeField(blank=True)
    discount_amount = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    percentual_discount = models.DecimalField(max_digits=4, decimal_places=3, blank=True, null=True)
    unit_discount = models.IntegerField(blank=True, null=True)
    amount_for_discount = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    unit_for_discount = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'{self.name} <{self.expiration_date.strftime('%d-%m-%Y')}>'

class Photo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    product = models.ForeignKey('Product', on_delete=models.CASCADE, blank=True, null=True, related_name='photos')
    type = models.ForeignKey('Type', on_delete=models.CASCADE, blank=True, null=True, related_name='photos')
    logo = models.ForeignKey('ShopConfig', on_delete=models.CASCADE, blank=True, null=True, related_name='photo')
    image = models.ImageField(upload_to='data/images/', null=True, blank=True)
    
    def __str__(self):
            return f'{self.name} <{self.product.name}>'