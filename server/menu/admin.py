from django.contrib import admin

from .models import Campaign, Ingredient, Photo, Product, Type

admin.site.register(Product)
admin.site.register(Type)
admin.site.register(Campaign)
admin.site.register(Photo)
admin.site.register(Ingredient)

