from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
# В базе данных должно быть 2 таблицы, одна для пользователей, а другая для самих заметок

class User(AbstractUser):
    """для пользователей"""
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True)
    first_name = models.CharField(max_length=20, unique=False)
    last_name = models.CharField(max_length=20, unique=False)
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
    class Meta:
        ordering = ('name',)
        index_together = (('id'),)#(('id', 'slug'),)

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

class User_adr(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.CharField(verbose_name='Город', max_length=128)
    street = models.CharField(verbose_name='Улица', max_length=128)
    apartment = models.CharField(verbose_name='Квартира', max_length=128)

class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return 'Order {}'.format(self.id)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.id)

    def get_cost(self):
        return self.price * self.quantity
