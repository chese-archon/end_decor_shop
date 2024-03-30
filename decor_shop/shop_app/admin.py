
from django.contrib import admin
from .models import Product, CartItem#, ProductImage
#from .urls import urlpatterns, path
from .views import statistic_view#, other_view1
# Register your models here.

#admin.site.register(Product)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'price')

admin.site.register(CartItem)

class MyAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            #path('statistic/', self.admin_view(urlpatterns)),
            #path('other-view1/', self.admin_view(other_view1)),
            # Добавьте другие настраиваемые URL-маршруты
        ]
        return my_urls + urls

my_admin_site = MyAdminSite(name='myadmin')