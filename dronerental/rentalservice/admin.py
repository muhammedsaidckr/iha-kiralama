from django.contrib import admin

from dronerental.rentalservice.models import Brand, Category, UAV

# Register your models here.
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(UAV)