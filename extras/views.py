from extras.models import Extra
from extras.forms import ExtraForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

# Create your views here.

def index(request):
    title = "Extralar&İçecekler"
    qy = Extra.objects.all()
    context = {
        "products":qy,
        "title": title
    }
    return render(request, "pages/extras.html",context)

def extrasWrap(request):
    title = "Dürümler"
    qy = Extra.objects.filter(category=title)
    context = {
        "products":qy,
        "title": title
    }
    return render(request, "pages/extras.html",context)

def extrasSnack(request):
    title = "Atıştırmalık & Sos"
    qy = Extra.objects.filter(category=title)
    context = {
        "products":qy,
        "title": title
    }
    return render(request, "pages/extras.html",context)

def extrasMacaroni(request):
    title = "Makarnalar"
    qy = Extra.objects.filter(category=title)
    context = {
        "products":qy,
        "title": title
    }
    return render(request, "pages/extras.html",context)

def extrasDrinks(request):
    title = "İçecekler"
    qy = Extra.objects.filter(category=title)
    context = {
        "products":qy,
        "title": title
    }
    return render(request, "pages/extras.html",context)

def extrasDesserts(request):
    title = "Tatlılar"
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
    qy = Extra.objects.all()

    context = {
        "extras":qy
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