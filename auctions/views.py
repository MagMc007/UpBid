from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.shortcuts import redirect, get_object_or_404
from .forms import ListingForm
from .models import User, Listings, WatchList, Bids, Category, Comments
from django.contrib.auth.decorators import login_required
from django.contrib import messages


def index(request):
    """renders page with active listings"""
    listings = Listings.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {"listings": listings})


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
            return render(
                request,
                "auctions/login.html",
                {"message": "Invalid username and/or password."},
            )
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
            return render(
                request, "auctions/register.html", {"message": "Passwords must match."}
            )

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(
                request,
                "auctions/register.html",
                {"message": "Username already taken."},
            )
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


""" a view to create new listings """


@login_required
def create_listing(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return redirect("index")
    else:
        form = ListingForm()
    return render(
        request,
        "auctions/create_listing.html",
        {
            "form": form,
        },
    )


""" this makes user view detail of a listing """


def detail_listing(request, pk):
    listing = Listings.objects.get(pk=pk)
    if not request.user.is_authenticated:
        return redirect("login")
    # for later watchlist purposes
    in_watchlist = WatchList.objects.filter(user=request.user, listing=listing).exists()
    # for the comments
    comments = Comments.objects.filter(on_item=pk)
    return render(
        request,
        "auctions/detail_view.html",
        {"listing": listing, 
         "in_watchlist": in_watchlist,
         "comments":comments
         },
    )


""" implemets watchlisting """


@login_required
def add_remove_watchlist(request, pk):
    item = get_object_or_404(Listings, pk=pk)

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "add":
            WatchList.objects.get_or_create(user=request.user, listing=item)
            return redirect("detail-listing", pk=pk)

        elif action == "remove":
            WatchList.objects.filter(user=request.user, listing=item).delete()
            return redirect("detail-listing", pk=pk)

    # If request is not POST or action is missing, just redirect back to listing
    return redirect("detail-listing", pk=pk)


""" all watchlists of a user """


@login_required
def detail_watchlist(request):
    watchlist_items = WatchList.objects.filter(user=request.user)
    # store all the watchlisted listings in this array
    listings = []

    for item in watchlist_items:
        listings.append(item.listing)

    return render(request, "auctions/watchlist.html", {"listings": listings})


""" handles biddings coming from user """


@login_required
def bid_on(request, pk):
    if request.method == "POST":
        bidder = request.user
        item = Listings.objects.get(pk=pk)
        # get the amount from form
        amount = float(request.POST.get("bid", "").strip())
        if amount > item.starting_bid:
            Bids.objects.get_or_create(bidder=bidder, listing=item, amount=amount)
            item.starting_bid = amount
            item.save()
            messages.success(request, "👍 Bid successful!")
        else:
            messages.error(request, "☠️ Bid higher!")
        return redirect("detail-listing", pk=pk)


""" implement category logic """


def list_category(request):
    categories = Category.objects.all()
    return render(request, "auctions/category.html", {"categories": categories})


""" display all the listing falling under the same category """


def detail_category_list(request, category):
    category_id = get_object_or_404(Category, category=category).id
    listings = Listings.objects.filter(category=category_id, is_active=True)
    return render(request, "auctions/detail_category_list.html", {"listings": listings})


"""" implements comments from users on product """


def comment_on(request, pk):
    if request.method == "POST":
        listing = get_object_or_404(Listings, pk=pk)
        content = request.POST.get("comment", "").strip()
        if content:
            Comments.objects.create(
                author=request.user,
                on_item=listing, 
                content=content)
        return redirect("detail-listing", pk=pk)
    


""" winner and close bid logic """


def close_bid(request, pk):
    if request.method == "POST":
        item = Listings.objects.get(pk=pk)
        item.is_active = False
        # winner logic 
        highest_bid = Bids.objects.filter(listing=item).order_by('-amount').first()
        if highest_bid:    
            item.winner =  highest_bid.bidder
        item.save()
        return redirect("detail-listing", pk=pk)
