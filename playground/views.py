from django.shortcuts import render
from django.db.models import Q, F, Value, Func, ExpressionWrapper
from django.db.models.aggregates import Count, Min, Max, Avg, Sum
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType
from django.db import transaction, connection


from store.models import Product, Order
from tags.models import TaggedItem

# Create your views here.
def say_hello(request):
    query_set= Product.objects.all()
    #query_set= Product.objects.filter(price__range=(20,30))
    #query_set= Product.objects.filter(collection__id__range=(1,2,3))
    #query_set= Product.objects.filter(title__icontains='cojin')
    #query_set= Product.objects.filter(title__startswith='cojin')
    #query_set= Product.objects.filter(last_update__year=2025)
    #query_set= Product.objects.filter(description__isnull=True)
    #query_set= Product.objects.filter(inventory__lt=10).filter(price__lt=20)
    #query_set= Product.objects.filter(Q(inventory__lt=10) | Q(price__lt=20)) or filter
    #query_set= Product.objects.filter(Q(inventory__lt=10) & Q(price__lt=20)) and filter
    #query_set= Product.objects.filter(Q(inventory__lt=10) & ~Q(price__lt=20)) negative filter
    #query_set= Product.objects.filter(inventory=F('collection__id')) where field equal to another field
    #query_set= Product.objects.filter(inventory__gt=1).orderby('title') ordering asc
    #query_set= Product.objects.filter(inventory__gt=1).orderby('-title') ordering desc
    #query_set= Product.objects.filter(inventory__gt=1).orderby('price','-title').reverse() multiple ordering and reversing the result
    #product= Product.objects.orderby('price')[0] get only first record
    #product= Product.objects.orderby('price')[:5] get first five records
    #query_set= Product.objects.orderby('price')[0:5] get first five records
    #query_set= Product.objects.earliest('price') get first record based on field
    #query_set= Product.objects.latest('price') get last record based on field
    #query_set= OrderItem.objects.values('product_id') get specific fields
    #query_set= OrderItem.objects.values('product_id').distinct() get specific fields get rid of duplicates
    #query_set= Product.objects.filter(id__in=OrderItem.objects.values('product_id').distinct()).orderby('title') get specific fields get rid of duplicates
    #query_set= Product.objects.only('id','title') get specific fields 
    #query_set= Product.objects.defer('description') get all except fields 
    
    #query_set= Product.objects.select_related('collection').all() # for foreign key relationships (1)
    #query_set= Product.objects.prefetch_related('promotions').all() # for foreign key relationships (*)
    #query_set= Product.objects.prefetch_related('promotions').select_related('collection').all() # for foreign key relationships (*)
    
    #product= Product.objects.get(pk=1,description__isnull=True)
    
    #result=Product.objects.aggregate(count=Count('id')) count ids
    #result=Product.objects.aggregate(min=Min('price')) get min price
    #result=Product.objects.aggregate(Max('price')) get max price
    #result=Product.objects.aggregate(Avg('price')) get average price
    #result=Product.objects.aggregate(Sum('price')) get sum of prices
    #result=Product.objects.aggregate(count=Count('id'),min_price=Min('price')) count ids
    #result=Product.objects.filter(collection__id=1).aggregate(count=Count('id'),min_price=Min('price')) count ids in collection 1
    
    #Customer.objects.annotate(is_new=Value(True)) add custom field
    #Customer.objects.annotate(new_id=F('id')+1) add custom field that have the value of id
    #Customer.objects.annotate(full_name=Func(F('first_name'),Value(' '),F('last_name'),function='CONCAT')) add custom field that is the concatenation of two fields
    #Customer.objects.annotate(full_name=Concat('first_name',Value(' '),'last_name') add custom field that is the concatenation of two fields
    #Customer.objects.annotate(orders_count=Count('order')) add custom field that count related orders
    #queryset=Product.objects.annotate( discounted_price=ExpressionWrapper(F('price')*0.8, output_field=models.DecimalField())) add custom field that calculate discounted price
    
    orders_query=Order.objects.select_related('customer').prefetch_related('orderitem_set__product').order_by('-placed_at')[:5]
    
    #Create Collection and insert to database
    #collection= Collection()
    #collection.title= "Video Games"
    #collection.featured_product= Product(pk=1)
    #or
    #collection= Collection(title="Video Games", featured_product= Product(pk=1))
    #collection.save()
    #or
    #collection= Collection.objects.create(title="Video Games", featured_product= Product(pk=1))
    #to see the id inserted collection.id
    
    #Update Collection
    #collection= Collection.objects.get(pk=10)
    #collection.featured_product= Product(pk=2)
    #collection.save()
    #or
    #Collection.objects.filter(pk=10).update(featured_product= Product(pk=3))
    
    #Delete Collection
    #collection= Collection.objects.get(pk=10)
    #collection.delete()
    #or
    #Collection.objects.filter(pk=10).delete()
    #Collection.objects.filter(id__gt=5).delete()
    
    #Transactions: Insert an order and its items and if one of the items fail the order should not be inserted
    #with transaction.atomic():
        #order= Order()
        #order.customer_id= 1
        #order.save()
        
        #item1= OrderItem()
        #item1.order= order
        #item1.product_id= 1
        #item1.quantity= 5
        #item1.price= 10
        #item1.save()
    #end with
    
    #raw sql query
    #query_set= Product.objects.raw('SELECT * FROM store_product')
    #or
    #cursor= connection.cursor()
    #cursor.execute('SELECT * FROM store_product')
    #query_set= cursor.fetchall()
    #cursor.close()
    #or
    #with connection.cursor() as cursor:
        #cursor.execute('SELECT * FROM store_product')
        #query_set= cursor.fetchall()
    return render(request, 'hello.html', {'name': "YASSINE", 'products': list(query_set), 'orders': list(orders_query)})

def tag_products(request):
    content_type=ContentType.objects.get_from_model(Product)
    tagged_items= TaggedItem.objects \
        .select_related('tag') \
        .filter(content_type=content_type, tag__label='Sports')
        
    #TaggedItem.objects.get_tags_for(Product, 1)
    return render(request, 'hello.html', {'name': "YASSINE"})