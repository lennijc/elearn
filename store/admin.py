from django.contrib import admin
from .models import (product,Customer,Order,collection,menus,courses,
                     categories,article,courseUser,comment,session,notification,
                     contact,orderModel,off)
# Register your models here.


admin.site.register(product)
admin.site.register(Customer)
# admin.site.register(Order)
admin.site.register(collection)
admin.site.register(menus)
admin.site.register(courses)
admin.site.register(categories)
admin.site.register(article)
admin.site.register(courseUser)
admin.site.register(comment)
admin.site.register(session)
admin.site.register(notification)
admin.site.register(contact)
admin.site.register(orderModel)
admin.site.register(off)
