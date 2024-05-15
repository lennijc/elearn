from django.contrib import admin
from .models import product,Customer,Order,collection,menus,courses,categories,article
# Register your models here.


admin.site.register(product)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(collection)
admin.site.register(menus)
admin.site.register(courses)
admin.site.register(categories)
admin.site.register(article)
