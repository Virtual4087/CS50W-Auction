from django.test import TestCase, Client
from .models import Listing, User, Bid, Category, Watchlist

# Create your tests here.

class Testing(TestCase):
    def setUp(self):
        user1 = User.objects.create(username="Tony")
        user2 = User.objects.create(username="Soprano")
        category = Category.objects.create(category = "protein")
        listing = Listing.objects.create(
            product="Egg", 
            description="It's a fucking egg. What else do ya wanna know?", 
            price= 40, 
            username = user1, 
            image="https://static.wikia.nocookie.net/egg-inc/images/e/e6/Egg_1.png/revision/latest?cb=20170221011545",
        ) 
        listing.categories.add(category)
        listing.save()
        Bid.objects.create(product=listing, username=user2, bid=70)
        Bid.objects.create(product=listing, username=user2, bid=100)
        Bid.objects.create(product=listing, username=user1, bid=2000)

    def test_category(self):
        """Checking categories"""
        category = Category.objects.first()
        self.assertEqual(category.category, "protein")
        self.assertEqual(category.categories.first().product, "Egg")

    def test_bidding(self):
        """Checking the highest bid and lowest bid of a listing"""
        c = Client()
        response = c.get("/")
        Highest_bid = response.context["listings"].first().product_bids.last()
        Lowest_bid = response.context["listings"].first().product_bids.first()
        self.assertEqual(Highest_bid.bid, 2000)
        self.assertEqual(Lowest_bid.bid, 70)

