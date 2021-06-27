from pizzas.models import CategoryManagment
from basket.models import BasketItem, OrderPizza
from extras.models import Extra
from extras.forms import ExtraForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.

def index(request):
    # url:/extras/ 
    title = "Extralar&İçecekler"
    keyword = request.GET.get("keyword")
    if keyword:
        qy = Extra.objects.filter(title__contains=keyword)
    else:
        qy = Extra.objects.all()
        
    category = CategoryManagment.objects.filter(kind="Ekstra")

    context = {
        "products":qy,
        "title": title,
        "categorys":category
    }
    return render(request, "pages/extras.html",context)

def categoryExtra(request,name):
    # url:/extras/name
    title = name
    keyword = request.GET.get("keyword")
    if keyword:
        qy = Extra.objects.filter(title__contains=keyword)
    else:
        qy = Extra.objects.filter(category=name)

    category = CategoryManagment.objects.filter(kind="Ekstra")

    context = {
        "products":qy,
        "title": title,
        "categorys":category
    }
    return render(request, "pages/extras.html",context)

def extrasWrap(request):
    # url:/extras/wraps
    title = "Dürümler"
    keyword = request.GET.get("keyword")
    if keyword:
        qy = Extra.objects.filter(title__contains=keyword, category=title)
    else:
        qy = Extra.objects.filter(category=title)
    context = {
        "products":qy,
        "title": title
    }
    return render(request, "pages/extras.html",context)

def extrasSnack(request):
    # url:/extras/atistirmaliklar
    title = "Atıştırmalık & Sos"
    keyword = request.GET.get("keyword")
    if keyword:
        qy = Extra.objects.filter(title__contains=keyword, category=title)
    else:
        qy = Extra.objects.filter(category=title)
    context = {
        "products":qy,
        "title": title
    }
    return render(request, "pages/extras.html",context)

def extrasMacaroni(request):
    # url:/extras/makarnalar
    title = "Makarnalar"
    keyword = request.GET.get("keyword")
    if keyword:
        qy = Extra.objects.filter(title__contains=keyword, category=title)
    else:
        qy = Extra.objects.filter(category=title)
    context = {
        "products":qy,
        "title": title
    }
    return render(request, "pages/extras.html",context)

def extrasDrinks(request):
    # url:/extras/icecekler
    title = "İçecekler"
    keyword = request.GET.get("keyword")
    if keyword:
        qy = Extra.objects.filter(title__contains=keyword, category=title)
    else:
        qy = Extra.objects.filter(category=title)
    context = {
        "products":qy,
        "title": title
    }
    return render(request, "pages/extras.html",context)

def extrasDesserts(request):
    # url:/extras/tatlilar
    title = "Tatlılar"
    keyword = request.GET.get("keyword")
    if keyword:
        qy = Extra.objects.filter(title__contains=keyword, category=title)
    else:
        qy = Extra.objects.filter(category=title)
    context = {
        "products":qy,
        "title": title
    }
    return render(request, "pages/extras.html",context)

@login_required(login_url="user:login")
def extras(request):
    # url:/extras/admin/extras/ 
    if not request.user.is_superuser:
        messages.info(request, "İzinsiz Giriş!")
        return redirect("/")
    
    keyword = request.GET.get("keyword")
    if keyword:
        qy = Extra.objects.filter(title__contains=keyword)
    else:
        qy = Extra.objects.all()

    context = {
        "extras":qy
    }
    return render(request,"user_operation/admin/extras.html",context)


@login_required(login_url="user:login")
def extraAdd(request):
    # url:/extras/admin/extras/add/
    if not request.user.is_superuser:
        messages.info(request,"İzinsiz Giriş!")
        return redirect("/")
    form = ExtraForm(request.POST or None)
    title = "Extra Ekle"
    context = {
        "title":title,
        "form":form
    }
    if form.is_valid():
        campaignModel = form.save(commit=False)
        campaignModel.save()
        messages.success(request,"Extra Eklendi")
        return redirect("/extras/admin/extras/")
    return render(request, "user_operation/admin/addProduct.html", context)

@login_required(login_url="user:login")
def extraEdit(request, id):
    # url:/extras/admin/extras/edit/<int:id>
    if not request.user.is_superuser:
        messages.info(request,"İzinsiz Giriş!")
        return redirect("/")
    extraModel = get_object_or_404(Extra,id = id)
    form = ExtraForm(request.POST or None, instance=extraModel)
    if form.is_valid():
        campaignModel = form.save(commit=False)
        campaignModel.save()
        messages.success(request, "Extra Başarıyla Güncellendi!")
        return redirect("/extras/admin/extras/")
    title = "Extra Düzenle"
    context = {
        "title":title,
        "form":form
    }
    return render(request, "user_operation/admin/editProducts.html", context)

@login_required(login_url="user:login")
def extraDelete(request, id):
    # url:/extras/admin/extras/delete/<int:id>
    if not request.user.is_superuser:
        messages.info(request,"İzinsiz Giriş!")
        return redirect("/")
    extraModel = get_object_or_404(Extra,id = id)
    orders = OrderPizza.objects.all()
    for i in orders:
        idList = list(eval(i.productIds))
        categoryList = list(eval(i.categoryIds))
        for j in range(len(idList)):
            if idList[j] == id and categoryList[j] == 2:
                i.delete()
    try:
        item = BasketItem.objects.get(productId=id)
        item.delete()
    except:
        pass
    extraModel.delete()
    messages.success(request,"Extra Silindi!.")
    return redirect("/extras/admin/extras/")