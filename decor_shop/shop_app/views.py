from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
#from .models import Note
from .models import User, Product, CartItem, User_adr, Order, OrderItem
from .cart import Cart
# , Note
from django.http import HttpResponseNotFound
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from .forms import ContactForm, OrderCreateForm
from django.contrib.auth import get_user_model

def authenticate(request, email=None, password=None):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(email=email)
    except UserModel.DoesNotExist:
        return None
    else:
        if user.check_password(password):
            return user
    return None

def contact_view(request):
    # если метод GET, вернем форму
    if request.method == 'GET':
        form = ContactForm()
    elif request.method == 'POST':
        # если метод POST, проверим форму и отправим письмо
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            from_email = form.cleaned_data['from_email']
            DEFAULT_FROM_EMAIL = from_email
            RECIPIENTS_EMAIL = ['afgnkad@gmail.com']#['luda1af@mail.ru']  # список почт получателей по уполчанию
            message = form.cleaned_data['message']
            try:
                send_mail(f'{subject} от {from_email}', message,
                          DEFAULT_FROM_EMAIL, RECIPIENTS_EMAIL)
            except BadHeaderError:
                return HttpResponse('Ошибка в теме письма.')
            return HttpResponse("<h3> Приняли! Спасибо за вашу заявку </h3>")#return redirect(success_view)#'success')
    else:
        return HttpResponse('Неверный запрос.')
    return render(request, "email.html", {'form': form})

def adres(request):
    if request.method == "GET":
        return render(request, "client_adr.html")
    else:
        data = request.POST
        #user = data.get("user")
        city = data.get("city")
        street = data.get("street")
        apartment = data.get("apartment")
        #if username is None:
        #    return HttpResponse("<h3>Введите имя пользователя</h3>")
        if city is None:
            return HttpResponse("<h3>Введите город</h3>")
        elif street is None:
            return HttpResponse("<h3>Введите first_name</h3>")
        elif apartment is None:
            return HttpResponse("<h3>Введите last_name</h3>")
        else:
            created = User_adr.objects.get_or_create(user=request.user,
                                                     city=city,
                                                     street=street,
                                                     apartment=apartment)
            #newuser.create_user(username, first_name, last_name, phone, email, password1)
            return HttpResponse(f"<h3>Введенный адрес: {city, street, apartment}</h3>")

def success_view(request):
    return #HttpResponse('Приняли! Спасибо за вашу заявку.')

def view_cart(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart_item, created = CartItem.objects.get_or_create(product=product,
                                                        user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))#return HttpResponse("<h3> Товар добавлен </h3>")#return redirect('cart.html')#cart:view_cart')


def remove_from_cart(request, item_id):
    cart_item = CartItem.objects.get(id=item_id)
    cart_item.delete()
    return redirect(view_cart)#redirect('cart.html')
def indexpage(request): # основная (home, /)
    return render(request, 'home.html')

def poiskpage(request): # поисковая страница + каталог
    if request.method == "GET":# request.method == "POST": GET
        return render(request, 'poisk.html')
    else:# request.method == "POST":
        query = request.POST.get('search_query')  # Получаем поисковой запрос из POST параметра
        results = Product.objects.filter(Q(name__icontains=query) | Q(type__icontains=query) | Q(description__icontains=query)) # Замените "title" на поле, по которому хотите производить поиск
        return render(request, 'poisk.html', {'results': results, 'query': query})


def decorpage(request): # весь декор
    types = ["свечи", "декор"]
    products = Product.objects.filter(type__in=types)#.all()
    return render(request, "decor.html", {"products": products})

def productpage(request):
    pass


def mebelpage(request): # мебель
    products = Product.objects.filter(type="мебель").all()
    return render(request, "mebel.html", {"products": products})

def candelpage(request): # свечи
    products = Product.objects.filter(type="свечи").all()
    return render(request, "candel.html", {"products": products})

def jewelypage(request): # украшения
    products = Product.objects.filter(type="украшения").all()
    return render(request, "jewely.html", {"products": products})


def regpage(request):  # регистрация
    if request.method == "GET":
        return render(request, "reg.html")
    else:
        data = request.POST
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        phone = data.get("phone")
        email = data.get("email")
        password1, password2 = data.get("password1"), data.get("password2")

        # Проверка наличия данных
        if not first_name:
            return HttpResponse("<h3>Введите имя</h3>")
        if not last_name:
            return HttpResponse("<h3>Введите фамилию</h3>")
        if not phone:
            return HttpResponse("<h3>Введите номер телефона</h3>")
        if not email:
            return HttpResponse("<h3>Введите почту</h3>")
        if not password1 or not password2:
            return HttpResponse("<h3>Введите пароль</h3>")
        if password1 != password2:
            return HttpResponse("<h3>Пароли должны совпадать</h3>")

        # Создание нового пользователя
        newuser = User.objects.create_user(username=email, email=email, password=password1, first_name=first_name,
                                           last_name=last_name)
        newuser.phone = phone
        newuser.save()
        return HttpResponse("<h3>Вы успешно зарегистрировались</h3>")


def lkpage(request): # lk, доступ только после регистрации
    if request.method == "GET":
        return render(request, "login.html")
    else:
        data = request.POST
        try:
            user = authenticate(request, email=data['email'], password=data['password'])
            if user is None:
                return HttpResponse(f"<h3>{data['email'], data['password']}Пользователь с таким логином и паролем не найден</h3>")
            login(request, user)
            return HttpResponse("<h3>Вы успешно авторизованы</h3>")
        except KeyError:
            return HttpResponse("<h3>Заполните все поля</h3>")

def logoutpage(request):
    logout(request)
    return render(request, "login.html")

def cartpage(request):  # корзина, доступ только после регистрации
    return render(request, 'index.html')

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                Order.objects.create(order=order,
                                     product=item['product'],
                                     price=item['price'],
                                     quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            return render(request, 'orders.html',
                          {'orders': Order.objects.filter(user=request.user)})
    else:
        form = OrderCreateForm
    return render(request, 'orders.html',
                  {'cart': cart, 'form': form})

def selectedpage(request): # избранное, доступ только после регистрации
    return render(request, 'index.html')

def user_orders(request):
    if request.method == "GET":
        orders = Order.objects.filter(user=request.user)
        if not orders:
            return render(request, 'orders.html', {'order_items': orders})
        else:
            total_price = sum(item.product.price * item.quantity for item in orders)
            order_date = orders.order_date
            return render(request, 'orders.html', {'order_items': orders,
                                               'total_price': total_price,
                                               'order_date': order_date})
    else:
        return render(request, 'orders.html')#redirect(productpage)

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # очистка корзины
            cart.clear()
            return render(request, 'orders.html',
                          {'order': order})
    else:
        form = OrderCreateForm
    return render(request, 'order_create.html',
                  {'cart': cart, 'form': form})

def statistic_view(request):
    #products = Product.objects.all()

    #return render(request, "statistic_view.html", {"products": products, })
    pass
