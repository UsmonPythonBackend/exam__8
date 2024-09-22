from django.urls import path
from .views import (IndexView, AboutView, ContactView, CartView, CheckoutView, ServiceView,
                    ShopView, ThankyouView, BlogView, LoginView, RegisterView)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('cart/', CartView.as_view(), name='cart'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('shop/', ShopView.as_view(), name='shop'),
    path('thankyou/', ThankyouView.as_view(), name='thankyou'),
    path('service/', ServiceView.as_view(), name='service'),
    path('blog/', BlogView.as_view(), name='blog'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),

]
