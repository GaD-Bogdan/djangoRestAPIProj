from django.contrib import admin

from .models import Item, Customer, Sale_record


admin.site.register(Item)
admin.site.register(Customer)
admin.site.register(Sale_record)
# Register your models here.
