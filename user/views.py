from basket.models import OrderPizza
from extras.models import Extra
from campaign.models import Campaign
from pizzas.models import Pizza
from basket.forms import AdminForm
from django.shortcuts import render,redirect
from .forms import LoginForm, RegisterForm, changeEmailForm, changePasswdForm, changeUsernameForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
import datetime




# Create your views here.
def register(request):
    # url:/user/register/
    if str(request.user) == "AnonymousUser": # kullanici giris yapmamissa True
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            newUser = User(username = username, first_name=first_name, last_name=last_name, email=email)
            newUser.set_password(password)
            try:
                newUser.save()
            except:
                messages.info(request,"Email Kullanılıyor.")
                return redirect("/user/register/")
            login(request,newUser)
            messages.success(request,"Kaydınız Başarılı! Artık Sizde PizzaS ailesindensiniz.")
            return redirect('/')
        
        form = RegisterForm()
        context = {
            "form": form
        }
        return render(request, "user_operation/normal_user/register.html", context)
    else:
        return redirect("/")

def loginUser(request):
    # url:/user/login/
    if(str(request.user) == "AnonymousUser"): # kullanici giris yapmamissa True
        form = LoginForm(request.POST or None)
        context={
            "form":form
        }
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username = username, password=password)
            if user is None:
                messages.info(request, "Email yada Parola Hatalı.")
                return render(request, "user_operation/normal_user/login.html", context)
            messages.success(request,"Giriş Başarılı! PizzaS'ın enfes pizza diyarlarında dolaşmaya hazır mısınız?")
            login(request, user)
            return redirect('/')
        
        return render(request, "user_operation/normal_user/login.html", context)
    return redirect("/")

def logoutUser(request):
    # url:/user/logout/
    if str(request.user) != "AnonymousUser": # kullanici giris yapmamissa False
        logout(request)
        messages.success(request,"Hesaptan Çıkış Yapıldı.")
    return redirect("/")

@login_required(login_url='user:login')
def profile(request):
    context = {
        "user": request.user
    }
    return render(request, "user_operation/normal_user/profile.html", context)

@login_required(login_url='user:login')
def myOrders(request):
    # url:/user/myaccount/siparislerim/
    """
        veritabanindan kullanicinin siparisleri cekilir. 98.satir
        ve ilgili listelere ilgili bilgiler atilir. - 104.satir
        (son 10 siparisi almak icin for dongusu 10.kere donunce kirilir)
        
        pizza bilgileri cekilir boya gore fiyatlar guncellenir - 111.satirdaki for dongusu
        tarihteki istenmeyen kisimlar sliding ile atilir - 129.satir
        butun bilgiler orderList listesinde toplanir - 131.satir
        tarihe gore siralamak icin reverse islemi yapilir - 132.satir
        sozluk yapisi ile arayuze gonderilir.

    """
    qy = OrderPizza.objects.filter(userId=request.user.id)
    productsIds = []
    orders = []
    categoryIds = []
    j = 0
    for i in qy: 
        productsIds.append(list(eval(i.productIds)))
        orders.append(i)
        categoryIds.append(list(eval(i.categoryIds)))
        j+=1
        if j>10:
            break
    ordersList = []
    x = 0
    for i in range(len(productsIds)):
        orders[x].productIds = []

        for j in range(len(productsIds[i])):  
            if categoryIds[i][j] == 1:  
                product = Pizza.objects.get(id=productsIds[i][j])
            elif categoryIds[i][j] == 2: 
                product = Campaign.objects.get(id=productsIds[i][j])
            elif categoryIds[i][j] == 3: 
                product = Extra.objects.get(id=productsIds[i][j])
            
            size = list(eval(orders[x].size))
            piece = list(eval(orders[x].piece))

            if size[j] == 2:
                product.price -= 10
            elif size[j] == 1:
                product.price -= 15
            product.price = round(product.price,2)
            item = [product,size[j], piece[j], categoryIds[i][j]]
            orders[x].productIds.append(item)
        orders[x].created_date = str(orders[x].created_date)[:16]
        ordersList.append(orders[x])
        x += 1
    user = User.objects.get(id=request.user.id)
    context = {
        "orders": ordersList,
        "user": user
    }
    return render(request, "user_operation/normal_user/myorders.html", context)

@login_required(login_url="user:login")
def adminDashboard(request):
    # url:/user/admin/dashboard/
    if request.user.is_superuser:
        qy = OrderPizza.objects.all()
        daily_earnings = 0
        monthly_income = 0
        annual_earnings = 0
        for i in qy:
            format = "%Y-%m-%d %H:%M:%S"
            dt_object = datetime.datetime.strptime(str(i.created_date)[:18], format)
            elapsed_time = datetime.datetime.now() - dt_object
            try:
                sure = int(str(elapsed_time).split()[0])
                if sure<30:
                    monthly_income += i.sum_price
                    annual_earnings += i.sum_price
                elif 30 < sure < 365:
                    annual_earnings += i.sum_price
            except:
                monthly_income += i.sum_price
                annual_earnings += i.sum_price
            if str(dt_object)[8:10] == str(datetime.datetime.now().date())[-2:] and str(dt_object)[:4] == str(datetime.datetime.now().date())[:4]:
                daily_earnings += i.sum_price
        context = {
            "yearly": annual_earnings,
            "monthly": monthly_income,
            "daily": daily_earnings
        }
        return render(request, "user_operation/admin/admin.html", context)
    else:
        messages.info("İzinsiz Giriş!")
        return redirect("/")

@login_required(login_url="user:login")
def orders(request):
    # url:/user/admin/orders/
    form = AdminForm(request.POST or None)
    if not request.user.is_superuser:
        messages.info(request,"İzinsiz Giriş!")
        return redirect("/")
    if form.is_valid():
        orderId = form.cleaned_data.get("orderId")
        status = form.cleaned_data.get("status")
        order = OrderPizza.objects.get(id=orderId)
        order.status = status
        order.save()
        return redirect("/user/admin/orders")
    qy = OrderPizza.objects.all()
    productsIds = []
    categoryIds = []
    orders = []
    j = 0
    for i in qy:
        productsIds.append(list(eval(i.productIds)))
        orders.append(i)
        categoryIds.append(list(eval(i.categoryIds)))
        j+=1
        if j>500:
            break
    ordersList = []
    x = 0
    for i in range(len(productsIds)):
        orders[x].productIds = []
        for j in range(len(productsIds[i])):     
            if categoryIds[i][j] == 1:
                product = Pizza.objects.get(id=productsIds[i][j])
            elif categoryIds[i][j] == 2:
                product = Campaign.objects.get(id=productsIds[i][j])
            else:
                product = Extra.objects.get(id=productsIds[i][j])
            
            size = list(eval(orders[x].size))
            piece = list(eval(orders[x].piece))

            if size[j] == 2:
                product.price -= 10
            elif size[j] == 1:
                product.price -= 15
            product.price = round(product.price,2)
            item = [product,size[j], piece[j]]
            orders[x].productIds.append(item)

        orders[x].created_date = str(orders[x].created_date)[:16]
        ordersList.append(orders[x])
        x += 1
    user = User.objects.get(id=request.user.id)
    full_name = user.first_name + " " + user.last_name
    context = {
        "orders": ordersList,
        "user": full_name,
        "form": form
    }
    return render(request, "user_operation/admin/orders.html",context)

@login_required(login_url="user:login")
def usernameChange(request):
    # url:/user/change/username/
    form = changeUsernameForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(username = str(request.user), password=password)
        if user is None:
            messages.info(request, "Parola Hatalı.")
            return render(request, "user_operation/normal_user/changeUsername.html", context) 
        user.username = username
        try:
            user.save()
        except:
            messages.info(request,"Kullanıcı adı zaten kullanımda")
            return redirect("/user/change/username")
        messages.success(request,"Kullanıcı Adınız Değiştirildi.")
        return redirect("/user/myaccount/")
    
    return render(request, "user_operation/normal_user/changeUsername.html", context)

@login_required(login_url="user:login")
def emailChange(request):
    # url:/user/change/email/
    form = changeEmailForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(username = str(request.user), password=password)
        if user is None:
            messages.info(request, "Parola Hatalı.")
            return render(request, "user_operation/normal_user/changeEmail.html", context) 
        user.email = email
        try:
            user.save()
        except:
            messages.info(request,"Email zaten kullanımda")
            return redirect("/user/change/username")
        messages.success(request,"Emailiniz Değiştirildi.")
        return redirect("/user/myaccount/")
    return render(request, "user_operation/normal_user/changeEmail.html", context)

@login_required(login_url="user:login")
def passwdChange(request):
    # url:/user/change/password/
    form = changePasswdForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        passwd = form.cleaned_data.get("password")
        newPasswd = form.cleaned_data.get("newPasswd")
        user = authenticate(username = str(request.user), password=passwd)
        if user is None:
            messages.info(request, "Eski Parola Hatalı.")
            return render(request, "user_operation/normal_user/changePasswd.html", context) 
        user.set_password(newPasswd)
        user.save()
        messages.success(request,"Şifreniz Değiştirildi.")
        return redirect("/user/myaccount/")
        
    return render(request, "user_operation/normal_user/changePasswd.html", context)


