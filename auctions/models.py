from django.contrib.auth.models import AbstractUser
from django.db import models


""" Abstract user for additional user fields if i want to"""


class User(AbstractUser):
    has_notifications = models.BooleanField(default=False)
    pass


""" class of a listing to be handled using category"""


class Category(models.Model):
    CATEGORY_CHOICES = [
        ('electronics', 'Electronics'),
        ('fashion', 'Fashion'),
        ('furniture', 'Furniture'),
        ('books', 'Books'),
        ('kitchen', 'Kitchen'),
        ('sports', 'Sports & Outdoors'),
        ('toys', 'Toys & Games'),
        ('beauty', 'Beauty & Health'),
    ]
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.category


""" item a user puts on the web for bidders to bid"""


class Listings(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    starting_bid = models.DecimalField(decimal_places=2, max_digits=10)
    image_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="lister")
    winner = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name="winner", blank=True, null=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, blank=True, null=True
    )

    def __str__(self):
        return self.title


""" bid created by user """


class Bids(models.Model):
    bidder = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="bids")
    listing = models.ForeignKey(Listings, on_delete=models.CASCADE, 
                                related_name="bids")
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bidder} on item {self.listing} at price of {self.amount}"


"""comment left on a listing """


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    on_item = models.ForeignKey(
        Listings, on_delete=models.SET_NULL, null=True, related_name="comments"
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} on item {self.on_item}"


"""for a page only logged in users can see like profile """


class WatchList(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="watchlist_items"
    )
    listing = models.ForeignKey(
        Listings, on_delete=models.CASCADE, related_name="watchlisted_by"
    )

    def __str__(self):
        return f"{self.user} watching {self.listing}"
