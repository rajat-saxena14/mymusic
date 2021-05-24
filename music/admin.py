from django.contrib import admin
from .models import Album,Song, Palbum, Plist, Orders, OrderUpdate
# Register your models here.
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(Palbum)
admin.site.register(Plist)
admin.site.register(Orders)
admin.site.register(OrderUpdate)
