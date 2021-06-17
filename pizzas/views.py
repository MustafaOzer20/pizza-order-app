from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import sqlite3
from basket.forms import BasketForm
from basket.models import BasketItem

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


# hazır decorators kullanımı - sepete ürün eklemek için giriş yapılmalı
# kullanıcı giriş yapmadıysa giriş sayfasına yönlendirilsin. 
@login_required(login_url='user:login')
def basket(request, id):
    # url:/pizzas/addtobasket/<int:id>
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
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    qy = cur.execute("SELECT * FROM pizzas_pizza where id = ?", (id,))
    for i in qy:  # i = (id,title,contents,price,imageUrl,category) type:tuple
        pizza = i
    form = BasketForm(request.POST or None)
    context = {
        "pizza": pizza,
        "form": form
    }
    cur.close()
    con.close()
    if form.is_valid():
        piece = form.cleaned_data.get("piece")
        size = form.cleaned_data.get("size")
        if not checkBasketItem(request.user.id, id, piece, size): # urunun aynisi sepette yoksa
            newBasketItem = BasketItem(userId = request.user.id,pizzaId=id,piece=piece,size=size)
            newBasketItem.save()
        messages.success(request,"Ürün Sepete Eklendi!")
        return redirect('/basket/basketItems/')
    return render(request, "pages/addtobasket.html", context)


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

def checkBasketItem(userId, pizzaId, piece, size):
    # urunun aynisi sepette varsa ve boylari ayniysa once adet guncellemesi yapar sonra true doner yoksa false doner
    con = sqlite3.connect("db.sqlite3")
    cur = con.cursor()
    qy = cur.execute("SELECT piece,size FROM basket_basketitem where userId=? and pizzaId=?",(userId,pizzaId))
    for item in qy: #item = (piece,size) type:tuple
        if size == item[1]:
            piece += item[0]
            cur.execute("UPDATE basket_basketitem SET piece=? where userId=? and pizzaId=? and size=?",(piece,userId,pizzaId,item[1]))
            con.commit()
            cur.close()
            con.close()
            return True
    cur.close()
    con.close()
    return False
