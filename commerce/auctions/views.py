from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import User, Listing, Category, Bid, Comment, Watchlist

def index(request):
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.all(),
        "search_for" : "Active Listings",
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)

        #Creating user's row in Watchlist
        temp = Watchlist()
        temp.username = request.user
        temp.save()
        
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def create_auction(request):
    
    if request.method == 'POST':

        # Creates a new listing and redirects the user to that listing page
        listing = Listing()
        listing.username = request.user
        listing.product = request.POST['title']
        listing.description = request.POST['description']
        listing.price = request.POST['price']
        listing.image = request.POST['image']
        listing.save()
        categories = request.POST.getlist('category')
        add = Category.objects.filter(pk__in=categories)
        listing.categories.set(add)

        return redirect("listing", product_id= listing.id)

    return render(request, "auctions/create_auction.html", {
        "categories" : Category.objects.all()
    })


def listing(request, product_id):  

    listing = Listing.objects.get(pk= product_id)
    highest_bid = listing.product_bids.last()
    comments = Comment.objects.filter(product= listing)

    # Check if user is authenticated and has a watchlist
    user_watchlist = None
    if request.user.is_authenticated:
        try:
            user_watchlist = Watchlist.objects.get(username=request.user)
        except Watchlist.DoesNotExist:
            # Create watchlist if it doesn't exist
            user_watchlist = Watchlist.objects.create(username=request.user)

        if request.method == 'POST':

            # Adds bid to a listing. If an user bids on the same listing again, the user's previous bidding is replaced by the new one
            if "bid" in request.POST:
                Bid.objects.filter(username= request.user, product= listing).delete()
                bid = int(request.POST["bid"])
                user_bid = Bid()
                user_bid.username = request.user
                user_bid.product = Listing.objects.get(pk=product_id)
                user_bid.bid = bid
                user_bid.save()
                return redirect("listing", product_id=product_id)
            
            # Adds comment to a listing
            if "comment" in request.POST:
                user_comment = request.POST["comment"]
                comment = Comment()
                comment.username = request.user
                comment.product = listing
                comment.comment = user_comment
                comment.save()
                return redirect("listing", product_id=product_id)
            
            # Closes an auction
            if "close" in request.POST:
                if request.user == listing.username:
                    listing.status = False
                    listing.save()
                    return redirect("index")

    return render(request, "auctions/listing.html", {
        "listing" : listing ,
        "highest_bid" : highest_bid,
        "watchlist" : listing in user_watchlist.product.all() if user_watchlist else False,
        "comments" : comments
    })

@login_required
def my_listings(request):
    return render(request, "auctions/index.html", {
        "listings" : Listing.objects.filter(username = request.user),
        "search_for" : "My Listings",
    })

@login_required
def history(request):
    purchases = []
    closed_listings = Listing.objects.filter(status= False)
    for listing in closed_listings:
        try:
            if listing.product_bids.last().username == request.user:
                purchases.append(listing.id)  
        except AttributeError:
            continue 

    return render(request, "auctions/index.html", {
        "listings" : closed_listings.filter(pk__in=purchases),
        "search_for" : "Purchase History",
    })

@login_required
def watchlist(request):
    
    user_watchlist = Watchlist.objects.get(username= request.user)

    if request.method == 'POST':
        listing = Listing.objects.get(pk=request.POST["listing"])
        if "add" in request.POST:
            user_watchlist.product.add(listing)
        elif "remove" in request.POST:
            user_watchlist.product.remove(listing)
        return redirect("listing", product_id=listing.id)

    return render(request, "auctions/index.html", {
        "listings" : user_watchlist.product.all(),
        "search_for" : "Watchlist",
    } )

def categories(request):
    if "category" in request.GET:
        selected_categories = request.GET.getlist("category")
        listings = Listing.objects.filter(categories__in = selected_categories).distinct()
                    
        return render(request, "auctions/index.html", {
            "listings" : listings,
            "search_for" : "Filter by Categories"
        })
    
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        "categories" : categories, 
    })