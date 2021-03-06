from pizzas.models import Pizza
from campaign.models import Campaign
from extras.models import Extra
from basket.models import BasketItem, OrderPizza
from basket.forms import BasketForm, CampaignBasketForm, OrderForm, OrderWithPaymentForm, PayMethodForm
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

@login_required(login_url="user:login")
def basketList(request):
    # url:/basket/basketItems
    """ 
        Sepetteki urunleri listeler
    """
    context = checkBasket(request)
    if context != None:
        form = PayMethodForm(request.POST or None)
        if form.is_valid():
            methodId = form.cleaned_data.get("payment_method")
            return redirect(f"/basket/payment/{methodId}")
        context.update({"form":form})
        return render(request, "pages/basket.html", context)
    return render(request, "pages/basket.html")

@login_required(login_url='user:login')
def delete(request, id):
    # url:/basket/basketItems/delete/<int:id>
    """ 
        Sepetten urun silme
    """
    item = BasketItem.objects.get(id=id)
    item.delete()
    return redirect("/basket/basketItems")

@login_required(login_url="user:login")
def payment(request, methodId):
    # url:/basket/payment/
    """ 
        Sepet bos ise ana sayfaya yonlendirir.
        Sepette urun varsa:
            1. get
                - formu gonder
            2. post
                - form bilgileri ile OrderPizza objesi olustur
                - objeyi veri tabanina kaydet
    """
    try:
        productId, basketId, size, pieces, sumPrice, categoryId = checkBasket(request, payment=True)
    except:
        messages.info(request,"Sepetiniz Boş")
        return redirect("/")
    if methodId == 3:
        form = OrderWithPaymentForm(request.POST or None)
    else:
        form = OrderForm(request.POST or None)

    if form.is_valid():
        adress = form.cleaned_data.get("adress")
        phone_number = form.cleaned_data.get("phone_number")
        user_note = form.cleaned_data.get("user_note")
        payment_method = methodId
        for i in range(len(productId)):
            if categoryId[i] == 1:
                pizza = Pizza.objects.get(id=productId[i])
                pizza.salesCount += pieces[i]
                pizza.save()
        productId = str(productId)   
        categoryId = str(categoryId)    
        newOrder = OrderPizza(
            basketId= basketId,user = request.user,
            productIds=productId, size=str(size),
            piece = str(pieces), sum_price = sumPrice,
            adress = adress, phone_number = phone_number,
            user_note = user_note,
            payment_method = payment_method,
            status=1,
            categoryIds = categoryId
            )
        newOrder.save()
        qy = BasketItem.objects.filter(user=request.user)
        for i in qy:
            i.delete()     
        messages.success(request,"Sipariş Verildi! Siparişiniz 30-40 dakika içerisinde size ulaşacaktır.")
        return redirect('/user/myaccount/siparislerim/')
    context = {
        "form": form
    }
    return render(request, "pages/payment.html", context )


@login_required(login_url="user:login")
def updateAddPiece(request, id):
    # url:/basket/basketItems/updatePiece/add/<int:id>
    return updatePiece(id, "+",request)

@login_required(login_url="user:login")
def updateReducePiece(request, id):
    # url:/basket/basketItems/updatePiece/reduce/<int:id>
    return updatePiece(id, "-",request)

@login_required(login_url='user:login')
def addToBasketCampaign(request, id):
    # url:/basket/addtobasket/campaign/<int:id>
    """
        gonderilen id ile urunun bilgilerini ceker
        1.get request
            - formu gonder
        2.post request
            - urunun aynisi sepette:(bu kontroller checkBasketItem fonksiyonu icinde yapiliyor.)
                a. varsa
                    i. boylari ayniysa urunun adetini guncelle
                    ii.boylari farkliysa urunu sepete ekle(farkli bir urunmus gibi)
                b. yoksa
                    i. sepete ekle
    """
    campaignModel = get_object_or_404(Campaign,id=id)
    form = CampaignBasketForm(request.POST or None)
    context = {
        "product": campaignModel,
        "form": form
    }
    if form.is_valid():
        piece = form.cleaned_data.get("piece")
        boolean, secondBool = checkBasketItem(request.user.id, id, piece,categoryId=2)
        if not boolean: # urunun aynisi sepette yoksa
            checkLimit = BasketItem.objects.filter(user=request.user)
            if len(checkLimit) >10:
                messages.info(request,"Sepete en fazla 10 ürün eklenebilir.")
                return redirect(f"/basket/addtobasket/campaign/{id}")
            newBasketItem = BasketItem(user = request.user,productId=id,piece=piece,size="-",categoryId=2)
            newBasketItem.save()
            messages.success(request,"Ürün Sepete Eklendi!")
        else:
            if secondBool:
                messages.info(request,"Bir Üründen Sepete En Fazla 20 Adet Eklenebilir!")
        return redirect('/basket/basketItems/')
    return render(request, "pages/addtobasket.html", context)

@login_required(login_url='user:login')
def addToBasketPizza(request, id):
    # url:/basket/addtobasket/pizza/<int:id>
    """
        gonderilen id ile urunun bilgilerini ceker
        1.get request
            - formu gonder
        2.post request
            - urunun aynisi sepette:(bu kontroller checkBasketItem fonksiyonu icinde yapiliyor.)
                a. varsa
                    i. boylari ayniysa urunun adetini guncelle
                    ii.boylari farkliysa urunu sepete ekle(farkli bir urunmus gibi)
                b. yoksa
                    i. sepete ekle
    """
    pizza = get_object_or_404(Pizza, id=id)
    form = BasketForm(request.POST or None)
    context = {
        "product": pizza,
        "form": form
    }
    if form.is_valid():
        piece = form.cleaned_data.get("piece")
        size = form.cleaned_data.get("size")
        boolean,secondBool = checkBasketItem(request.user, id, piece, size)
        if not boolean: # urunun aynisi sepette yoksa
            checkLimit = BasketItem.objects.filter(user=request.user)
            if len(checkLimit) >10:
                messages.info(request,"Sepete en fazla 10 ürün eklenebilir.")
                return redirect(f"/basket/addtobasket/pizza/{id}")
            newBasketItem = BasketItem(user = request.user,productId=id,piece=piece,size=size, categoryId=1)
            newBasketItem.save()
            messages.success(request,"Ürün Sepete Eklendi!")
        else:
            if secondBool:
                messages.info(request,"Bir Üründen Sepete En Fazla 20 Adet Eklenebilir!")
        return redirect('/basket/basketItems/')
    return render(request, "pages/addtobasket.html", context)


@login_required(login_url='user:login')
def addToBasketExtras(request, id):
    # url:/basket/addtobasket/extras/<int:id>
    """
        gonderilen id ile urunun bilgilerini ceker
        1.get request
            - formu gonder
        2.post request
            - urunun aynisi sepette:(bu kontroller checkBasketItem fonksiyonu icinde yapiliyor.)
                a. varsa
                    i. boylari ayniysa urunun adetini guncelle
                    ii.boylari farkliysa urunu sepete ekle(farkli bir urunmus gibi)
                b. yoksa
                    i. sepete ekle
    """
    extra = get_object_or_404(Extra, id=id)
    form = CampaignBasketForm(request.POST or None)
    context = {
        "product": extra,
        "form": form
    }
    if form.is_valid():
        piece = form.cleaned_data.get("piece")
        boolean, secondBool = checkBasketItem(request.user, id, piece, categoryId=3)
        if not boolean: # urunun aynisi sepette yoksa
            checkLimit = BasketItem.objects.filter(user=request.user)
            if len(checkLimit) >10:
                messages.info(request,"Sepete en fazla 10 ürün eklenebilir.")
                return redirect(f"/basket/addtobasket/extras/{id}")
            newBasketItem = BasketItem(user = request.user,productId=id,piece=piece,size="-", categoryId=3)
            newBasketItem.save()
            messages.success(request,"Extra Sepete Eklendi!")
        else:
            if secondBool:
                messages.info(request,"Bir Üründen Sepete En Fazla 20 Adet Eklenebilir!")
        
        return redirect('/basket/basketItems/')
    return render(request, "pages/addtobasket.html", context)



#functions

def checkBasketItem(user, productId, piece, size=None, categoryId=None):
    # urunun aynisi sepette varsa ve boylari ayniysa once adet guncellemesi yapar sonra true doner yoksa false doner
    if categoryId == None:
        qy = BasketItem.objects.filter(user=user,productId=productId)
    else:
        qy = BasketItem.objects.filter(user=user,productId=productId, categoryId=categoryId)
    for item in qy:
        if size == item.size:
            item.piece += piece
            if item.piece > 20:
                item.piece=20
                item.save()
                return [True,True]
            item.save()
            return [True,False]
        if size==None:
            item.piece += piece
            if item.piece > 20:
                item.piece=20
                item.save()
                return [True,True]
            item.save()
            return [True,False]
    return [False,False]

def checkBasket(request, payment=False):
    # basketteki urunleri, urun sayisini ve toplam fiyati sozluk yapisinda doner
    # eger basket bossa None doner
    query = BasketItem.objects.filter(user=request.user)
    productId = []
    basketLs = []
    pieces = []
    size = []
    categoryId = []
    basketId = -1
    sumPrice = 0
    for item in query:
        productId.append(item.productId)
        basketLs.append(item)
        pieces.append(item.piece)
        try:
            size.append(int(item.size))
        except:
            size.append("-")
        basketId = item.id
        categoryId.append(item.categoryId)
    if len(basketLs) > 0:
        productItems = []
        x = 0
        for i in range(len(productId)):
            if categoryId[i] == 1:
                product = Pizza.objects.get(id=productId[i])
            elif categoryId[i] == 2:
                product = Campaign.objects.get(id=productId[i])
            else:
                product = Extra.objects.get(id=productId[i])
            if basketLs[x].size == '2': #orta boy
                product.price -= 10
            elif basketLs[x].size == '1': #kucuk boy
                product.price -= 15

            product.price = round(product.price,2)
            sumPrice += product.price * int(pieces[x])
            productItems.append(product)
                
            x+=1
        sumPrice = round(sumPrice,2)
        basketItems = list(zip(productItems, basketLs))
        if payment:
            return [productId, basketId, size, pieces, sumPrice, categoryId]
        context = {
            "basketItems": basketItems,
            "itemsCount": len(basketItems),
            "sumPrices": sumPrice,
        }
        return context
    return None



def updatePiece(id,operation,request):
    # verilen idye gore sepetteki urunun adet guncellemesini yapar
    # operation '+' ise mevcut adete 1 ekler.
    # operation '-' ise mevcut adeti 1 eksiltir.
    # eger urun adeti 1 iken eksiltme islemi yapilirsa urun sepetten kaldirilir. 
    item = BasketItem.objects.get(id=id)
    if operation == "+":
        item.piece += 1
        if item.piece >20:
            item.piece = 20
            messages.info(request,"Bir üründen en fazla 20 tane sipariş edilebilir!")
        item.save()
    else:
        item.piece -= 1
        item.save()
        if item.piece <= 0:
            print("delete")
            item.delete()
    
    return redirect("/basket/basketItems/")

