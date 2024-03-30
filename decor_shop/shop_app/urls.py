from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .admin import my_admin_site

urlpatterns = [
    path("", views.indexpage, name="home"),
    path("home/", views.indexpage, name="home"),
    path("home", views.indexpage, name="home"),
    path("reg", views.regpage, name="reg"),
    path("reg/", views.regpage, name="reg"),#regpage
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    #path("cart_add/(?P<product_id>\d+)/$", views.views.cart_add, name="cart_add"),
    #path("cart_remove/(?P<product_id>\d+)/$", views.views.cart_remove, name="cart_remove"),
    path("login/", views.lkpage, name="login"),
    path("login", views.lkpage, name="login"),
    path("logout/", views.logoutpage, name="logout"),
    path("logout", views.logoutpage, name="logout"),
    ####
    path("decor", views.decorpage, name="decor"),
    path("decor/", views.decorpage, name="decor"),
    path("mebel", views.mebelpage, name="mebel"),
    path("mebel/", views.mebelpage, name="mebel"),
    path("jewely", views.jewelypage, name="jewely"),
    path("jewely/", views.jewelypage, name="jewely"),
    path("candel", views.candelpage, name="candel"),
    path("candel/", views.candelpage, name="candel"),
    path("poisk", views.poiskpage, name="poisk"),
    path("poisk/", views.poiskpage, name="poisk"),
    ##
    path("email", views.contact_view, name="email"),
    path("email/", views.contact_view, name="email"),
    path("adr/", views.adres, name="adr"),
    path("adr", views.adres, name="adr"),
    path('create/', views.order_create, name='order_create'),
    #path('orders/', views.user_orders, name="orders"),
    #path('orders', views.user_orders, name="orders"),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)