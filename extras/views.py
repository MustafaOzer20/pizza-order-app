from extras.models import Extra
from extras.forms import ExtraForm
import sqlite3
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.

def index(request):
    title = "Extralar&İçecekler"
    qy = query()
    context = {
        "products":qy,
        "title": title
    }
    return render(request, "pages/extras.html",context)

def extrasWrap(request):
    title = "Dürümler"
    qy = query(category="Dürümler")
    context = {
        "products":qy,
        "title": title
    }
    return render(request, "pages/extras.html",context)

def extrasSnack(request):
    title = "Atıştırmalık & Sos"
    qy = query(category="Atıştırmalık & Sos")
    context = {
        "products":qy,
        "title": title
    }
    return render(request, "pages/extras.html",context)

def extrasMacaroni(request):
    title = "Makarnalar"
    qy = query(category="Makarnalar")
    context = {
        "products":qy,
        "title": title
    }
    return render(request, "pages/extras.html",context)

def extrasDrinks(request):
    title = "İçecekler"
    qy = query(category="İçecekler")
    context = {
        "products":qy,
        "title": title
    }
    return render(request, "pages/extras.html",context)

def extrasDesserts(request):
    title = "Tatlılar"
    qy = query(category="Tatlılar")
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
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    qy = cur.execute("SELECT * FROM extras_extra")
    extrasList = []
    for i in qy:
        extrasList.append(i)
    context = {
        "extras":extrasList
    }
    return render(request,"user_operation/admin/extras.html",context)


@login_required(login_url="user:login")
def extraAdd(request):
    # url:/user/admin/campaign/add/
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
    # url:/user/admin/campaign/edit/<int:id>
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
    # url:/user/admin/campaign/delete/<int:id>
    if not request.user.is_superuser:
        messages.info(request,"İzinsiz Giriş!")
        return redirect("/")
    extraModel = get_object_or_404(Extra,id = id)
    extraModel.delete()
    messages.success(request,"Extra Silindi!.")
    return redirect("/extras/admin/extras/")
    
# functions
def query(category=None):
    # kategoriye gore sorgu yapar.
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    if category == None:
        query = cur.execute("SELECT * FROM extras_extra")
    else:
        query = cur.execute("SELECT * FROM extras_extra where category = ?", (category,))
    return query