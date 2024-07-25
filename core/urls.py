from django.urls import path
from core import views


# list of all urls of core app

urlpatterns = [
    path('', views.HomePageView.as_view(), name="home_page"),
    path('about/', views.AboutPageView.as_view(), name="about_page"),
    path('contact/', views.ContactPageView.as_view(), name="contact_page"),
    path('product-detail/<int:pk>/', views.ProduceDetailView.as_view(), name="product_detail"),
    path('add-to-cart/', views.AddToCartView.as_view(), name="add_to_cart"),
    path('show-cart/', views.show_cart, name="show_cart"),
    path('plus-cart/', views.plus_cart_view, name="plus_cart"),
    path('minus-cart/', views.minus_cart_view, name="minus_cart"),
    path('remove-cart/', views.remove_cart_view, name="remove_cart"),
    path('checkout/', views.checkout_view.as_view(), name="checkout_view"),
    path('payment-done/', views.payment_done_view.as_view(), name="payment_done"),
    path('order-placed/', views.order_placed_view.as_view(), name="order_placed"),

]
