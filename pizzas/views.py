from django.contrib.auth.models import User
from user.forms import OrderRatings
from pizzas.forms import PizzaForm
from pizzas.models import CategoryManagment, Pizza, ProductsRatings
from basket.models import BasketItem, OrderPizza
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
    category = CategoryManagment.objects.filter(kind="Pizza")
    return render(request, 'pages/pizzas.html', {"pizzas" : pizzas, "title": title, "categorys":category})

def pizzasCategory(request,name):
    # url:/pizzas/
    title = name
    keyword = request.GET.get("keyword")
    if not keyword:
        pizzas = Pizza.objects.filter(category=name)
    else:
        pizzas = Pizza.objects.filter(title__contains=keyword)
    category = CategoryManagment.objects.filter(kind="Pizza")
    return render(request, 'pages/pizzas.html', {"pizzas" : pizzas, "title": title, "categorys":category})



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
        return redirect("/pizzas/admin/products/")
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
        return redirect("/pizzas/admin/products/")
    return render(request, "user_operation/admin/addProduct.html", context)

@login_required(login_url="user:login")
def productsDelete(request, id):
    # url:/pizzas/admin/products/delete/<int:id>
    if not request.user.is_superuser:
        messages.info(request,"İzinsiz Giriş!")
        return redirect("/")
    pizza = get_object_or_404(Pizza,id=id)
    orders = OrderPizza.objects.all()
    try:
        item = BasketItem.objects.get(productId=id,categoryId=1)
        item.delete()
    except:
        pass
    for i in orders:
        idList = list(eval(i.productIds))
        categoryList = list(eval(i.categoryIds))
        for j in range(len(idList)):
            if idList[j] == id and categoryList[j]==1:
                i.delete()
    pizza.delete()
    messages.success(request,"Ürün Silindi!.")
    return redirect("/pizzas/admin/products/")


@login_required(login_url="user:login")
def ratingPizza(request,id):
    orders = OrderPizza.objects.filter(userId=request.user.id)
    result = False
    for i in orders:
        idList = list(eval(i.productIds))
        categoryList = list(eval(i.categoryIds))
        for j in range(len(idList)):
            if idList[j] == id and categoryList[j] == 1:
                result = True
    if not result:
        messages.info(request,"Bu ürünü değerlendirebilmek için en az 1 kere bu üründen satın almalısınız!")
        return redirect(f"/basket/addtobasket/pizza/{id}")
    form = OrderRatings(request.POST or None)
    pizza = get_object_or_404(Pizza,id=id)
    context = {
        "form":form,
        "product":pizza
    }
    if form.is_valid():
        comment = form.cleaned_data.get("comments")
        rating = form.cleaned_data.get("rating")
        try:
            history = ProductsRatings.objects.get(user=request.user, product = pizza, categoryId=1)
            history.comment = comment
            history.rating = rating
            history.save()
        except:
            ratingsModel = ProductsRatings(comment=comment,ratings=rating,categoryId=1,product=pizza,user=request.user)
            ratingsModel.save()
        ratings = ProductsRatings.objects.filter(product = pizza)
        count = 0
        sumRating = 0
        for i in ratings:
            sumRating+=i.ratings
            count+=1
        pizza.forRating = str(sumRating/count)
        pizza.save()
        messages.success(request,"Değerlendirmeniz Gönderildi")
        return redirect("/pizzas/user/ratings")
    return render(request,"pages/ratings.html",context)

@login_required(login_url="user:login")
def myRatings(request):
    ratings = ProductsRatings.objects.filter(user=request.user)
    context = {"ratings":ratings}
    return render(request,"user_operation/normal_user/myratings.html",context)

def pizzasRatings(request,id):
    pizza = Pizza.objects.get(id=id)
    comments = ProductsRatings.objects.filter(product=pizza)
    context = {
        "product":pizza,
        "comments":comments,
        "lengthComment":len(comments)
    }
    return render(request,"pages/productRatings.html",context)