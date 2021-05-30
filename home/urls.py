from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='home'),
    path("about", views.about, name='about'),
    path("contact", views.contact, name='contact'),
    path("reviews", views.reviews, name='reviews'),
    path("book/<str:pk>/",views.viewBook, name='book'),
    path("register", views.register, name='register'),
    path("sign_in",  views.sign_in, name='sign_in'),
    path("logout",   views.logoutUser, name='logout'),
    path("sell", views.sell, name='sell'),
    path("cart", views.cart, name='cart'),
    path("update_item/", views.updateItem, name='update_item'),
    path("checkout", views.checkout, name='checkout'),
    path("process_order/", views.proccessOrder, name='process_order'),
    path("misc/", views.misc, name='misc'),
    path("privacypolicy/", views.privacypolicy, name='privacypolicy'),
    path("termsandconditions/", views.terms, name='terms'),
    path("disclaimer/", views.disclaimer, name='disclaimer'),
]   