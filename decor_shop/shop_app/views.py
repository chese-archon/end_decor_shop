from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
#from .models import Note
from .models import User, Product, CartItem
from .cart import Cart
# , Note
from django.http import HttpResponseNotFound


from django.db.models import Q


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

def regpage(request): # регистрация
    if request.method == "GET":
        return render(request, "reg.html")
    else:
        data = request.POST
        username = data.get("username")
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        phone = data.get("phone")
        email = data.get("email")
        password1, password2 = data.get("password1"), data.get("password2")
        if username is None:
            return HttpResponse("<h3>Введите имя пользователя</h3>")
        elif email is None:
            return HttpResponse("<h3>Введите почту</h3>")
        elif first_name is None:
            return HttpResponse("<h3>Введите first_name</h3>")
        elif last_name is None:
            return HttpResponse("<h3>Введите last_name</h3>")
        elif password1 is None or password2 is None:
            return HttpResponse("<h3>Введите пароль</h3>")
        elif password1 != password2:
            return HttpResponse("<h3>Пароли должны совпадать</h3>")
        else:
            newuser = User()
            newuser.create_user(username, first_name, last_name, phone, email, password1)
            return HttpResponse("<h3>Вы успешно зарегистрировались</h3>")

def lkpage(request): # lk, доступ только после регистрации
    if request.method == "GET":
        return render(request, "login.html")
    else:
        data = request.POST
        try:
            user = authenticate(request, username=data['username'], password=data['password'])
            if user is None:
                return HttpResponse("<h3>Пользователь с таким логином и паролем не найден</h3>")
            login(request, user)
            return HttpResponse("<h3>Вы успешно авторизованы</h3>")
        except KeyError:
            return HttpResponse("<h3>Заполните все поля</h3>")

def logoutpage(request):
    logout(request)
    return render(redirect, "login.html")

def cartpage(request): # корзина, доступ только после регистрации
    return render(request, 'index.html')

def selectedpage(request): # избранное, доступ только после регистрации
    return render(request, 'index.html')
