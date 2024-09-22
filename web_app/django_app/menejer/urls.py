from django.urls import path
from .views import LoginAdminView, RegisterAdminView, IndexAdminView, ShopAdminView

from django.urls import path
from .views import ShopAdminView, FurnitureUpdateView, FurnitureDeleteView

urlpatterns = [
    path('shopadmin/', ShopAdminView.as_view(), name='shop_admin'),
    path('shopadmin/update/<str:id>/', FurnitureUpdateView.as_view(), name='furniture_update'),
    path('shopadmin/delete/<str:id>/', FurnitureDeleteView.as_view(), name='furniture_delete'),
    path('index_admin/', IndexAdminView.as_view(), name='index_admin'),
    path('loginadmin/', LoginAdminView.as_view(), name='login_admin'),
    path('registeradmin/', RegisterAdminView.as_view(), name='register_admin'),
    path('shopadmin/', ShopAdminView.as_view(), name='shop_admin'),
]
