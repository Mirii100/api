from django.contrib import admin
from .models import Profile,Category,Item,Review,Order,OrderItem,Notification
# Register your models here.
admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Item)
admin.site.register(Review)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Notification)