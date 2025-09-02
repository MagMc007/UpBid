from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("create/", views.create_listing, name="create-listing"),
    path("<int:pk>/", views.detail_listing, name="detail-listing"),
    path("<int:pk>/watchlist/", views.add_remove_watchlist, name="watch-list"),
    path("watchlist/", views.detail_watchlist, name="detail-watchlist"),
]
