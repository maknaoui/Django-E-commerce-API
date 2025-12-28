from django.contrib import admin, messages
from . import models
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse

class InventoryFilter(admin.SimpleListFilter):
    title = 'inventory'
    parameter_name = 'inventory'
    def lookups(self, request, model_admin):
        return [
            ('<10', 'Low'),
            ('>=10', 'OK')
        ]
        
    def queryset(self, request, queryset):
        if self.value() == '<10':
            return queryset.filter(inventory__lt=10)
        if self.value() == '>=10':
            return queryset.filter(inventory__gte=10)

#Google DjangoModelAdmin to customize the admin interface
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # to fill the slug with the title automatically :  prepopulated_fields = {'slug': ['title']}
    autocomplete_fields=['collection']
    actions = ['clear_inventory']
    #To show only this fields :  fields = ['title', 'description', 'price', 'inventory', 'collection', 'promotions', 'last_updated']
    #To exclude some fields : 
    exclude = ['promotions']
    #readonly_fields = ['last_updated']
    list_display = ['title', 'price', 'collection_title','inventory_status']
    list_editable = ['price']
    list_filter = [InventoryFilter,'collection', 'promotions']
    list_per_page = 10
    search_fields = ['title']
    list_select_related = ['collection']
    
    def collection_title(self, product):
        return product.collection.title
    
    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'Low'
        return 'OK'
    
    @admin.action(description='Clear inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were successfully updated.',
            messages.SUCCESS
        )

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    autocomplete_fields=['customer']
    list_display = ['id', 'customer', 'placed_at', 'payment_status']
    list_per_page = 10
    list_editable = ['payment_status']
    search_fields = ['customer__first_name', 'customer__last_name']
    list_select_related = ['customer']
    
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership', 'orders_count']
    list_editable = ['membership']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']
    
    @admin.display(ordering='orders_count')
    def orders_count(self, customer):
        url=(reverse('admin:store_order_changelist') 
             + '?'
             + urlencode({'customer__id': str(customer.id)}))
        return format_html('<a href="{}">{}</a>', url, customer.orders_count)
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            orders_count=Count('order')
        )


# Register your models here.
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']
    search_fields = ['title']
    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url=(reverse('admin:store_product_changelist') 
             + '?'
             + urlencode({'collection__id': str(collection.id)}))
        return format_html('<a href="{}">{}</a>', url, collection.products_count)
    
    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )
    