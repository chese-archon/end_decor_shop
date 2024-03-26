from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# В базе данных должно быть 2 таблицы, одна для пользователей, а другая для самих заметок

class User(AbstractUser):
    """для пользователей"""
    pass
    def create_user(self, first_name, last_name, phone, email, password):
        #self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.email = email
        self.set_password(password)
        self.save()

class Product(models.Model):
    """Товар"""

    name = models.CharField(verbose_name='Название', max_length=128)#, db_index=True)
    type = models.CharField(verbose_name='Тип', max_length=128)
    price = models.IntegerField(default=0) #цена
    height = models.IntegerField(default=0)
    width = models.IntegerField(default=0)
    depth = models.IntegerField(default=0)
    description = models.TextField(default='') #описание
    image = models.ImageField(upload_to='product_images', null=True) #Фотография товара

    def __str__(self):
        return self.name

    #def new_product(self, data):
    #    product = Product()
    #    product.text = data['note-text']
        #product.user = self
    #    product.save()

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.quantity} x {self.product.name}'

class Selected(models.Model):
    """для продуктов в избранном"""
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='selected_items')