from django.contrib import admin

from .models import Item, Order, OrderItem, Address


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'ordered'
                    'address'
                    ]
    list_display_links = [
        'user',
        'address'
    ]
    list_filter = ['ordered']
    search_fields = [
        'user__username',
        'ref_code'
    ]


class AddressAdmin(admin.ModelAdmin):
    list_display = [
        'user',
        'street_address',
        'apartment_address',
        'country',
        'post_code',
        'default'
    ]
    list_filter = ['default', 'country']
    search_fields = ['user', 'street_address',
                     'apartment_address', 'post_code']


admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Address, AddressAdmin)
