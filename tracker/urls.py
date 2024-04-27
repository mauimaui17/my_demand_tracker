from django.urls import path
from . import views

urlpatterns = [
    path("add-to-cart/", views.addToCart, name="add-to-cart"),
    path("remove-from-cart/", views.removeFromCart, name="remove-from-cart"),
    path("profile/", views.profile, name="profile"),
    path("home/", views.homepage, name="homepage"),
    path("", views.index, name="tracker")
]
