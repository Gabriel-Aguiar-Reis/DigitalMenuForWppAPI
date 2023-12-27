import uuid

from django.db import models


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    type = models.ForeignKey('Type', on_delete=models.CASCADE, blank=True, null=True)
    promotion = models.ForeignKey('Campaign', on_delete=models.CASCADE, blank=True, null=True)
    percentual_margin = models.DecimalField(max_digits=4, decimal_places=3)
    cost_price = models.DecimalField(max_digits=6, decimal_places=2)
    
    def __str__(self):
        return f'<{self.type.name}> {self.name}'

class Type(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    promotion = models.ForeignKey('Campaign', on_delete=models.CASCADE, blank=True, null=True)
    percentual_margin = models.DecimalField(max_digits=4, decimal_places=3)
    
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
    image = models.ImageField(upload_to='data/images/', null=True, blank=True)
    
    def __str__(self):
            return f'{self.name} <{self.product.name}>'