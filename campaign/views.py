from django.shortcuts import render,redirect,get_object_or_404
import sqlite3
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from campaign.forms import CampaignForm, Campaign

# Create your views here.

def index(request):
    # url:/campaign/
    title = "Kampanyalar"
    qy = query()
    return render(request, 'pages/campaign.html', {"pizzas" : qy, "title": title})

def campaignWrap(request):
    # url:/campaign/wrap
    title = "Dürümler"
    qy = query(category="Dürümler")
    return render(request, 'pages/campaign.html', {"pizzas" : qy, "title": title})

def campaignPizzas(request):
    # url:/campaign/pizzas
    title = "Pizzalar"
    qy = query(category="Pizzalar")
    return render(request, 'pages/campaign.html', {"pizzas" : qy, "title": title})

def campaignMacaroni(request):
    # url:/campaign/pizzas
    title = "Makarnalar"
    qy = query(category="Makarnalar")
    return render(request, 'pages/campaign.html', {"pizzas" : qy, "title": title})

def campaignSpecial(request):
    # url:/campaign/pizzas
    title = "Özel Fırsatlar"
    qy = query(category="Özel Fırsatlar")
    return render(request, 'pages/campaign.html', {"pizzas" : qy, "title": title})

@login_required(login_url="user:login")
def campaign(request):
    # url:/campaign/admin/campaign/ 
    if not request.user.is_superuser:
        messages.info(request, "İzinsiz Giriş!")
        return redirect("/")
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    qy = cur.execute("SELECT * FROM campaign_campaign")
    campaignList = []
    for i in qy:
        campaignList.append(i)
    context = {
        "campaigns":campaignList
    }
    return render(request,"user_operation/admin/campaign.html",context)

@login_required(login_url="user:login")
def campaignAdd(request):
    # url:/user/admin/campaign/add/
    if not request.user.is_superuser:
        messages.info(request,"İzinsiz Giriş!")
        return redirect("/")
    form = CampaignForm(request.POST or None)
    title = "Kampanya Ekle"
    context = {
        "title":title,
        "form":form
    }
    if form.is_valid():
        campaignModel = form.save(commit=False)
        campaignModel.save()
        messages.success(request,"Kampanya Eklendi")
        return redirect("/campaign/admin/campaign/")
    return render(request, "user_operation/admin/addProduct.html", context)

@login_required(login_url="user:login")
def campaignEdit(request, id):
    # url:/user/admin/campaign/edit/<int:id>
    if not request.user.is_superuser:
        messages.info(request,"İzinsiz Giriş!")
        return redirect("/")
    campaignModel = get_object_or_404(Campaign,id = id)
    form = CampaignForm(request.POST or None, instance=campaignModel)
    if form.is_valid():
        campaignModel = form.save(commit=False)
        campaignModel.save()
        messages.success(request, "Kampanya Başarıyla Güncellendi!")
        return redirect("/campaign/admin/campaign/")
    title = "Kampanya Düzenle"
    context = {
        "title":title,
        "form":form
    }
    return render(request, "user_operation/admin/editProducts.html", context)

@login_required(login_url="user:login")
def campaignDelete(request, id):
    # url:/user/admin/campaign/delete/<int:id>
    if not request.user.is_superuser:
        messages.info(request,"İzinsiz Giriş!")
        return redirect("/")
    campaignModel = get_object_or_404(Campaign,id = id)
    campaignModel.delete()
    messages.success(request,"Kampanya Silindi!.")
    return redirect("/campaign/admin/campaign/")



# functions

def query(category=None):
    # kategoriye gore sorgu yapar.
    con = sqlite3.connect('db.sqlite3')
    cur = con.cursor()
    if category == None:
        query = cur.execute("SELECT * FROM campaign_campaign")
    else:
        query = cur.execute("SELECT * FROM campaign_campaign where category = ?", (category,))
    return query