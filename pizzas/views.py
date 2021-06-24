from pizzas.forms import PizzaForm
from pizzas.models import Pizza
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render


# Create your views here.

def index(request):
    # url:/
    return redirect("/pizzas/")


def pizzas(request):
    # url:/pizzas/
    title = "Tüm Pizzalar"
    keyword = request.GET.get("keyword")
    if not keyword:
        pizzas = Pizza.objects.all()
    else:
        pizzas = Pizza.objects.filter(title__contains=keyword)
    return render(request, 'pages/pizzas.html', {"pizzas" : pizzas, "title": title})

def cazip(request):
    # url:/pizzas/cazip/
    title = "Cazip Pizzalar"
    keyword = request.GET.get("keyword")
    if not keyword:
        pizzas = Pizza.objects.filter(category=title)
    else:
        pizzas = Pizza.objects.filter(category=title,title__contains=keyword)
    return render(request, 'pages/pizzas.html', {"pizzas" : pizzas, "title":title})

def special(request):
    # url:/pizzas/special/
    title = "Özel Pizzalar"
    keyword = request.GET.get("keyword")
    if not keyword:
        pizzas = Pizza.objects.filter(category=title)
    else:
        pizzas = Pizza.objects.filter(category=title,title__contains=keyword)
    return render(request, 'pages/pizzas.html', {"pizzas" : pizzas, "title" : title})

def bolmalzeme(request):
    # url:/pizzas/bolmalzemeli/
    title = "Bol Malzemeli Pizzalar"
    keyword = request.GET.get("keyword")
    if not keyword:
        pizzas = Pizza.objects.filter(category=title)
    else:
        pizzas = Pizza.objects.filter(category=title,title__contains=keyword)
    return render(request, 'pages/pizzas.html', {"pizzas" : pizzas, "title": title})

def gurme(request):
    # url:/pizzas/gurme/
    title = "Gurme Pizzalar"
    keyword = request.GET.get("keyword")
    if not keyword:
        pizzas = Pizza.objects.filter(category=title)
    else:
        pizzas = Pizza.objects.filter(category=title,title__contains=keyword)
    return render(request, 'pages/pizzas.html', {"pizzas" : pizzas, "title":title})


@login_required(login_url="user:login")
def products(request):
    # url:/pizzas/admin/products/
    if not request.user.is_superuser:
        messages.info(request,"İzinsiz Giriş!")
        return redirect("/")
    keyword = request.GET.get("keyword")
    if keyword:
        qy = Pizza.objects.filter(title__contains = keyword)
    else:
        qy =  Pizza.objects.all()
    context = {
        "pizzas":qy
    } 
    return render(request, "user_operation/admin/products.html", context)

@login_required(login_url="user:login")
def productsEdit(request, id):
    # url:/pizzas/admin/products/edit/<int:id>
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
    # url:/pizzas/admin/products/add/
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
    # url:/pizzas/admin/products/delete/<int:id>
    if not request.user.is_superuser:
        messages.info(request,"İzinsiz Giriş!")
        return redirect("/")
    pizza = get_object_or_404(Pizza,id=id)
    pizza.delete()
    messages.success(request,"Ürün Silindi!.")
    return redirect("/user/admin/products/")

