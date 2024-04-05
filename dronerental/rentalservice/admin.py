from django.contrib import admin

from dronerental.rentalservice.models import Brand, Category, UAV, RentalTransaction

# Register your models here.
admin.site.register(Brand)
admin.site.register(Category)
admin.site.register(UAV)
admin.site.register(RentalTransaction)
admin.site.site_header = 'İHA Kiralama Yönetim Paneli'
admin.site.site_title = 'İHA Kiralama Yönetim Paneli'
admin.site.index_title = 'İHA Kiralama Yönetim Paneli'
admin.site.description = 'İHA Kiralama Yönetim Paneli'