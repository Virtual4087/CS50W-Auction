from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    pass

class Listing(models.Model):
    status = models.BooleanField(default=True)
    date = models.DateTimeField(default= datetime.now())
    product = models.CharField(max_length=64)
    description = models.TextField(max_length=1000)
    price = models.IntegerField()
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_listings" )
    image = models.URLField(blank=True, max_length=1000)
    categories = models.ManyToManyField('Category', blank=True, related_name="categories")

    def __str__(self):
        return f"{self.product} was put on auction by {self.username.username}"

class Category(models.Model):
    category = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.category}"

class Bid(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_bids")
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="product_bids")
    bid = models.IntegerField()

    def __str__(self):
        return f"{self.username} made a bid of {self.bid} for {self.product.product}"


class Comment(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    product = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="product_comments")
    comment = models.TextField(max_length=1000)

    def __str__(self):
        return f"{self.username} made a comment saying \"{self.comment}\" on {self.product.product}"
    
class Watchlist(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_watchlist", unique=True)
    product = models.ManyToManyField(Listing, blank=True, related_name="watchlisted_by")