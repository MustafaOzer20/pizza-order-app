from sqlite3.dbapi2 import connect
from basket.models import OrderPizza
from basket.forms import OrderForm, OrderWithPaymentForm, PayMethodForm
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
import sqlite3
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
    con = sqlite3.connect("db.sqlite3")
    deleteFunc(id,con)
    con.close()
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
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    try:
        pizzasId, basketId, size, pieces, sumPrice = checkBasket(request, payment=True)
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
        pizzasId = str(pizzasId)       
        newOrder = OrderPizza(
            basketId= basketId,userId = request.user.id,
            pizzasIds=pizzasId, size=str(size),
            piece = str(pieces), sum_price = sumPrice,
            adress = adress, phone_number = phone_number,
            user_note = user_note,
            payment_method = payment_method,
            status=1
            )
        newOrder.save()
        qy = cur.execute("SELECT id FROM basket_basketitem where userId=?",(request.user.id,))
        for i in qy: # i = (id,)
            deleteFunc(i[0],con)      
        messages.success(request,"Sipariş Verildi! Siparişiniz 30-40 dakika içerisinde size ulaşacaktır.")
        cur.close()
        con.close()
        return redirect('/user/myaccount/siparislerim/')
    context = {
        "form": form
    }
    cur.close()
    con.close()
    return render(request, "pages/payment.html", context )


@login_required(login_url="user:login")
def updateAddPiece(request, id):
    # url:/basket/basketItems/updatePiece/add/<int:id>
    """ 
        Kullanici admin degilse ana sayfaya yonlendirir.
        Kullanici admin ise updatePiece fonksiyonu cagrilir.
    """
    if request.user.is_superuser:
        return updatePiece(id, "+")
    messages.info(request,"İzinsiz Giriş!")
    return redirect("/")

@login_required(login_url="user:login")
def updateReducePiece(request, id):
    # url:/basket/basketItems/updatePiece/reduce/<int:id>
    """ 
        Kullanici admin degilse ana sayfaya yonlendirir.
        Kullanici admin ise updatePiece fonksiyonu cagrilir.
    """
    if request.user.is_superuser:
        return updatePiece(id, "-")
    messages.info(request,"İzinsiz Giriş!")
    return redirect("/")



#functions

def checkBasket(request, payment=False):
    # basketteki urunleri, urun sayisini ve toplam fiyati sozluk yapisinda doner
    # eger basket bossa None doner
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    query = cur.execute("SELECT * FROM basket_basketitem where userId = ?", (request.user.id,))
    pizzasId = []
    basketLs = []
    pieces = []
    size = []
    basketId = -1
    sumPrice = 0
    for item in query:
        pizzasId.append(item[1])   #item = (id,pizzaid,piece,size,userId)
        basketLs.append(item)
        pieces.append(item[2])
        size.append(int(item[3]))
        basketId = item[0]
    
    if len(basketLs) > 0:
        pizzaItems = []
        x = 0
        for i in pizzasId:
            qy = cur.execute("SELECT * FROM pizzas_pizza where id = ?", (i,))
            for j in qy:
                temp = list(j) # j = (id,title,contents,price,imageUrl,category)
                if basketLs[x][3] == '2': #orta boy
                    temp[3] -= 10
                elif basketLs[x][3] == '1': #kucuk boy
                    temp[3] -= 15
                temp[3] = round(temp[3],2)
                pizzaItems.append(temp)
                sumPrice += temp[3] * int(pieces[x])
            x+=1
        sumPrice = round(sumPrice,2)
        basketItems = list(zip(pizzaItems, basketLs))
        if payment:
            return [pizzasId, basketId, size, pieces, sumPrice]
        
        context = {
            "basketItems": basketItems,
            "itemsCount": len(basketItems),
            "sumPrices": sumPrice,
        }
        cur.close()
        con.close()
        return context
    cur.close()
    con.close()
    return None


def deleteFunc(id, con):
    # verilern id ve sql baglantisi ile sepetten urun siler
    cur = con.cursor()
    cur.execute("DELETE FROM basket_basketitem where id = ?", (id,))
    con.commit()
    cur.close()


def updatePiece(id,operation):
    # verilen idye gore sepetteki urunun adet guncellemesini yapar
    # operation '+' ise mevcut adete 1 ekler.
    # operation '-' ise mevcut adeti 1 eksiltir.
    # eger urun adeti 1 iken eksiltme islemi yapilirsa urun sepetten kaldirilir. 
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    qy = cur.execute("SELECT piece FROM basket_basketitem where id=?",(id,))
    for i in qy: # i = (piece,) type:tuple
        if operation == "+":
            piece = i[0] + 1
        else:
            piece = i[0] - 1
    if piece <= 0:
        cur.close()
        con.close()
        return redirect("/basket/basketItems/delete/{}".format(id))
    else:
        cur.execute("UPDATE basket_basketitem SET piece=? where id=?",(piece,id))
        con.commit()
    cur.close()
    con.close()
    return redirect("/basket/basketItems/")

