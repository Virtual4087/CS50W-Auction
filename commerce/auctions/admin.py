from django.contrib import admin
from auctions.models import User, Listing, Category, Bid, Comment, Watchlist
# Register your models here.

admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Category)
admin.site.register(Bid)
admin.site.register(Comment)
admin.site.register(Watchlist)