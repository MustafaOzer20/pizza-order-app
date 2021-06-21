from pizzas.forms import PizzaForm
from pizzas.models import Pizza
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
import sqlite3


# Create your views here.

def index(request):
    # url:/
    return redirect("/pizzas/")


def pizzas(request):
    # url:/pizzas/
    title = "Tüm Pizzalar"
    qy = query()
    return render(request, 'pages/pizzas.html', {"pizzas" : qy, "title": title})

def cazip(request):
    # url:/pizzas/cazip/
    title = "Cazip Pizzalar"
    qy = query(title)
    return render(request, 'pages/pizzas.html', {"pizzas" : qy, "title":title})

def special(request):
    # url:/pizzas/special/
    title = "Özel Pizzalar"
    qy = query(title)
    return render(request, 'pages/pizzas.html', {"pizzas" : qy, "title" : title})

def bolmalzeme(request):
    # url:/pizzas/bolmalzemeli/
    title = "Bol Malzemeli Pizzalar"
    qy = query(title)
    return render(request, 'pages/pizzas.html', {"pizzas" : qy, "title": title})

def gurme(request):
    # url:/pizzas/gurme/
    title = "Gurme Pizzalar"
    qy = query(title)
    return render(request, 'pages/pizzas.html', {"pizzas" : qy, "title":title})


@login_required(login_url="user:login")
def products(request):
    # url:/user/admin/products/
    if not request.user.is_superuser:
        messages.info(request,"İzinsiz Giriş!")
        return redirect("/")
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    qy = cur.execute("SELECT * FROM pizzas_pizza")
    pizzas = []
    for i in qy:
        pizzas.append(i)

    context = {
        "pizzas":pizzas
    } 
    cur.close()
    con.close()
    return render(request, "user_operation/admin/products.html", context)

@login_required(login_url="user:login")
def productsEdit(request, id):
    # url:/user/admin/products/edit/<int:id>
    if not request.user.is_superuser:
        messages.info(request,"İzinsiz Giriş!")
        return redirect("/")
    pizza = get_object_or_404(Pizza,id = id)
    form = PizzaForm(request.POST or None, instance=pizza)
    if form.is_valid():
        pizza = form.save(commit=False)
        pizza.save()
        messages.success(request, "Ürün Başarıyla Güncellendi!")
        return redirect("/user/admin/products/")
    title = "Pizza Düzenle"
    context = {
        "title":title,
        "form":form
    }
    return render(request, "user_operation/admin/editProducts.html", context)

@login_required(login_url="user:login")
def productsAdd(request):
    # url:/user/admin/products/add/
    if not request.user.is_superuser:
        messages.info(request,"İzinsiz Giriş!")
        return redirect("/")
    form = PizzaForm(request.POST or None)
    title = "Pizza Ekle"
    context = {
        "title":title,
        "form":form
    }
    if form.is_valid():
        pizza = form.save(commit=False)
        pizza.save()
        messages.success(request,"Ürün Eklendi")
        return redirect("/user/admin/products/")
    return render(request, "user_operation/admin/addProduct.html", context)

@login_required(login_url="user:login")
def productsDelete(request, id):
    # url:/user/admin/products/delete/<int:id>
    if not request.user.is_superuser:
        messages.info(request,"İzinsiz Giriş!")
        return redirect("/")
    pizza = get_object_or_404(Pizza,id=id)
    pizza.delete()
    messages.success(request,"Ürün Silindi!.")
    return redirect("/user/admin/products/")


#functions

def query(category=None):
    # kategoriye gore sorgu yapar.
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    if category == None:
        query = cur.execute("SELECT * FROM pizzas_pizza")
    else:
        query = cur.execute("SELECT * FROM pizzas_pizza where category = ?", (category,))
    return query

