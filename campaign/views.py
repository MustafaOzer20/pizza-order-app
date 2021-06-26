from basket.models import BasketItem, OrderPizza
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from campaign.forms import CampaignForm, Campaign

# Create your views here.

def index(request):
    # url:/campaign/
    title = "Kampanyalar"
    keyword = request.GET.get("keyword")
    if keyword:
        qy = Campaign.objects.filter(title__contains=keyword)
    else:
        qy = Campaign.objects.all()
    return render(request, 'pages/campaign.html', {"campaigns" : qy, "title": title})

def campaignWrap(request):
    # url:/campaign/wrap
    title = "Dürümler"
    keyword = request.GET.get("keyword")
    if keyword:
        qy = Campaign.objects.filter(title__contains=keyword, category=title)
    else:
        qy = Campaign.objects.filter(category=title)
    return render(request, 'pages/campaign.html', {"campaigns" : qy, "title": title})

def campaignPizzas(request):
    # url:/campaign/pizzas
    title = "Pizzalar"
    keyword = request.GET.get("keyword")
    if keyword:
        qy = Campaign.objects.filter(title__contains=keyword, category=title)
    else:
        qy = Campaign.objects.filter(category=title)
    return render(request, 'pages/campaign.html', {"campaigns" : qy, "title": title})

def campaignMacaroni(request):
    # url:/campaign/makarnalar
    title = "Makarnalar"
    keyword = request.GET.get("keyword")
    if keyword:
        qy = Campaign.objects.filter(title__contains=keyword, category=title)
    else:
        qy = Campaign.objects.filter(category=title)
    return render(request, 'pages/campaign.html', {"campaigns" : qy, "title": title})

def campaignSpecial(request):
    # url:/campaign/special
    title = "Özel Fırsatlar"
    keyword = request.GET.get("keyword")
    if keyword:
        qy = Campaign.objects.filter(title__contains=keyword, category=title)
    else:
        qy = Campaign.objects.filter(category=title)
    return render(request, 'pages/campaign.html', {"campaigns" : qy, "title": title})

@login_required(login_url="user:login")
def campaign(request):
    # url:/campaign/admin/campaign/ 
    if not request.user.is_superuser:
        messages.info(request, "İzinsiz Giriş!")
        return redirect("/")
    keyword = request.GET.get("keyword")
    if keyword:
        qy = Campaign.objects.filter(title__contains=keyword)
    else:
        qy = Campaign.objects.all()
    context = {
        "campaigns":qy
    }
    return render(request,"user_operation/admin/campaign.html",context)

@login_required(login_url="user:login")
def campaignAdd(request):
    # url:/campaign/admin/campaign/add/
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
    # url:/campaign/admin/campaign/edit/<int:id>
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
    # url:/campaign/admin/campaign/delete/<int:id>
    if not request.user.is_superuser:
        messages.info(request,"İzinsiz Giriş!")
        return redirect("/")
    campaignModel = get_object_or_404(Campaign,id = id)
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
    campaignModel.delete()
    messages.success(request,"Kampanya Silindi!.")
    return redirect("/campaign/admin/campaign/")