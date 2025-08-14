from django.contrib import admin
from .models import Category, Listings, Bids, Comments, WatchList


admin.site.register(Category)
admin.site.register(Listings)
admin.site.register(Bids)
admin.site.register(Comments)
admin.site.register(WatchList)
