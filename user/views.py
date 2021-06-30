from pizzas.forms import CategoryForm, CategoryFormWithoutKind
from basket.models import  BasketItem, OrderPizza
from extras.models import Extra
from campaign.models import Campaign
from pizzas.models import CategoryManagment, Pizza, ProductsRatings
from basket.forms import AdminForm
from django.shortcuts import get_object_or_404, render,redirect,HttpResponse
from .forms import ChangeForgotPasswd, ForgetPasswdForm, LoginForm, OrderRatings, RegisterForm, changeEmailForm, changePasswdForm, changeUsernameForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout,get_user_model
from django.contrib.auth.decorators import login_required
import datetime
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .tokens import account_activation_token
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_text
from django.template.loader import render_to_string


# Create your views here.
def register(request):
    # url:/user/register/
    if str(request.user) == "AnonymousUser": # kullanici giris yapmamissa True
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            username = form.cleaned_data.get("username")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            password = form.cleaned_data.get("password")
            user = User(username=username, first_name=first_name, last_name=last_name, email=email)
            user.set_password(password)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your account.'
            message = render_to_string('email_template.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
            })
            send_mail(mail_subject, message, 'pizzaspizza.company@gmail.com', [email])
            return HttpResponse('Please confirm your email address to complete the registration')
        context = {
            "form": form
        }
        return render(request, "user_operation/normal_user/register.html", context)
    else:
        return redirect("/")

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request,"Thank you for your email confirmation. Now you can login your account.")
        login(request,user)
        return redirect("/")
    else:
        return HttpResponse('Activation link is invalid!')


def forgetPassword(request):
    form = ForgetPasswdForm(request.POST or None)
    context = {"form":form}
    if form.is_valid():
        email = form.cleaned_data.get("email")
        try:
            user = User.objects.get(email=email)
        except:
            messages.info(request,"Böyle Bir Kullanıcı Bulunamadı")
            return redirect("/user/login")
        current_site = get_current_site(request)
        mail_subject = 'Change Password'
        message = render_to_string('passwd_template.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
        })
        send_mail(mail_subject, message, 'pizzaspizza.company@gmail.com', [email])
        messages.success(request,'Mailinize link gönderildi. Linke tıklayarak şifrenizi değiştirebilirsiniz.')
        return redirect('/user/login/')

    return render(request,"user_operation/normal_user/forgotPasswd.html",context)

def changePasswdtoForget(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        form = ChangeForgotPasswd(request.POST or None)
        context = {"form":form}
        if form.is_valid():
            password = form.cleaned_data.get("password")
            user.set_password(password)
            user.save()
            messages.success(request,"Şifreniz Başarıyla Değiştirildi")
            login(request,user)
            return redirect("/")
        return render(request,"user_operation/normal_user/changePasswd.html",context)
    else:
        return HttpResponse('Geçersiz URL!')

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
    form = OrderRatings(request.POST or None)
    qy = OrderPizza.objects.filter(user=request.user)
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
        "user": user,
        "form":form
    }
    return render(request, "user_operation/normal_user/myorders.html", context)


from django.db.models import Max, Min
def statistic():
    orders = OrderPizza.objects.all()
    productPieces = 0
    for i in orders:
        pieceList = list(eval(i.piece))
        for j in pieceList:
            productPieces += j

    best_selling = Pizza.objects.aggregate(Max('salesCount'))
    worst_selling = Pizza.objects.aggregate(Min('salesCount'))
    popular = Pizza.objects.aggregate(Max('forRating'))
    unpopular = Pizza.objects.aggregate(Min('forRating'))

    popular_pizza = Pizza.objects.filter(forRating=popular['forRating__max'])
    popular_pizza = popular_pizza[0]
    unpopular_pizza = Pizza.objects.filter(forRating=unpopular['forRating__min'])
    unpopular_pizza = unpopular_pizza[0]

    best_pizza = Pizza.objects.filter(salesCount=best_selling['salesCount__max'])
    best_pizza = best_pizza[0]


    worst_pizza = Pizza.objects.filter(salesCount=worst_selling['salesCount__min'])
    worst_pizza = worst_pizza[0]

    return best_pizza,worst_pizza, popular_pizza, unpopular_pizza, productPieces


@login_required(login_url="user:login")
def adminDashboard(request):
    # url:/user/admin/dashboard/
    if request.user.is_superuser:
        qy = OrderPizza.objects.all()
        best_pizza, worst_pizza, popular_pizza, unpopular_pizza, productPieces = statistic()
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
        
        annual_earnings = round(annual_earnings,2)
        monthly_income = round(monthly_income,2)
        daily_earnings = round(daily_earnings,2)
        context = {
            "yearly": annual_earnings,
            "monthly": monthly_income,
            "daily": daily_earnings,
            "best_pizza":best_pizza,
            "popular_pizza":popular_pizza,
            "unpopular_pizza":unpopular_pizza,
            "worst_pizza":worst_pizza,
            "lengthOrders":len(qy),
            "sumProductPieces":productPieces
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
    user = request.user
    email = request.user.email
    current_site = get_current_site(request)
    mail_subject = 'Change Email.'
    message = render_to_string('changeEmail_template.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    send_mail(mail_subject, message, 'pizzaspizza.company@gmail.com', [email])
    messages.success(request,'Mailinize link gönderildi. Linke tıklayarak emailinizi değiştirebilirsiniz.')
    return redirect("/user/myaccount")

@login_required(login_url="user:login")
def emailChangeToken(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        form = changeEmailForm(request.POST or None)
        context = {"form":form,"title":"Email Değiştir"}
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            controlUser = authenticate(username = str(request.user), password=password)
            if controlUser == user:
                user.email = email
                user.save()
                messages.success(request,"Emailiniz Başarıyla Değiştirildi")
                login(request,user)
                return redirect("/user/myaccount")
        return render(request,"user_operation/normal_user/changePasswd.html",context)
    else:
        return HttpResponse('Activation link is invalid!')

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


@login_required(login_url="user:login")
def listCategories(request):
    if not request.user.is_superuser:
        messages.info(request,"İzinsiz Giriş!")
        return redirect("/")
    keyword = request.GET.get("keyword")
    if keyword:
        categories = CategoryManagment.objects.filter(name__contains=keyword)
    else:
        categories = CategoryManagment.objects.all()
    context = {
        "categorys":categories
    }
    return render(request,"user_operation/admin/categories.html",context)

def checkCategory(name,kind):
    try:
        control = CategoryManagment.objects.get(name=name)
        if control.kind == kind:
            return True
        else:
            raise Exception("Kategori Eklenebilir.")
    except:
        return False


@login_required(login_url="user:login")
def addCategory(request):
    if not request.user.is_superuser:
        messages.info(request,"İzinsiz Giriş!")
        return redirect("/")
    form = CategoryForm(request.POST or None)
    if form.is_valid():
        name = form.cleaned_data.get("name")
        kind = form.cleaned_data.get("kind")
        if checkCategory(name,kind):
            messages.info(request,"Böyle bir kategori zaten var!")
            return redirect("/user/admin/categories/add/")
        else:
            newCategory = CategoryManagment(name=name,kind=kind)
            newCategory.save()
            messages.success(request,"Kategori başarıyla eklendi.")
            return redirect("/user/admin/categories/")
    context = {
        "form":form
    }
    return render(request,"user_operation/admin/addProduct.html",context)


@login_required(login_url="user:login")
def editCategory(request,id):
    if not request.user.is_superuser:
        messages.info(request,"İzinsiz Giriş!")
        return redirect("/")

    category = get_object_or_404(CategoryManagment,id=id)
    form = CategoryFormWithoutKind(request.POST or None, instance=category)
    if form.is_valid():
        name = form.cleaned_data.get("name")
        if checkCategory(name,category.kind):
            messages.info(request,"Böyle bir kategori zaten var!")
            return redirect(f"/user/admin/categories/edit/{id}")
        else:
            updatePizzas(id,name)
            category.save()
            messages.success(request,"Kategori başarıyla eklendi.")
            return redirect("/user/admin/categories/")

    context = {"form":form,"title":"Kategori Düzenle"}
    return render(request,"user_operation/admin/editProducts.html",context)

def updatePizzas(id,newName):
    oldCategory = CategoryManagment.objects.get(id=id)
    product = getProduct(oldCategory.name,oldCategory.kind)
    for i in product:
        i.category = newName
        i.save()

def getProduct(name,kind):
    if kind == "Pizza":
        product = Pizza.objects.filter(category=name)
    elif kind == "Kampanya":
        product = Campaign.objects.filter(category=name)
    else:
        product = Campaign.objects.filter(category=name)
    return product


@login_required(login_url="user:login")
def deleteCategory(request,id):
    if not request.user.is_superuser:
        messages.info(request,"İzinsiz Giriş!")
        return redirect("/")

    category = get_object_or_404(CategoryManagment,id=id)
    products = getProduct(category.name,category.kind)
    product_orders = OrderPizza.objects.all()
    ids = []
    for i in products:
        ids.append(i.id)
        # v eğer sepette bu kategorideki bir pizza varsa sepetten bu ürün silinecek
        try:
            item = BasketItem.objects.get(productId=i.id)
            item.delete()
        except:
            pass
        
        if category.kind == "Pizza":
            # v pizzaların içindeki ratingler silinecek 
            ratings = ProductsRatings.objects.filter(productId=i.id)
            for x in ratings:
                x.delete()

        #   kategori içindeki pizzalar silinecek
        i.delete()
    
    #   eğer daha önce bu kategorideki bir pizza sipariş edilmiş ise o sipariş silinecek
    kind = {1:"Pizza",2:"Kampanya",3:"Ekstra"}

    for i in product_orders:
        productIds = list(eval(i.productIds))
        categoryIds = list(eval(i.categoryIds))
        for x in range(len(productIds)):
            if (productIds[x] in ids) and kind[categoryIds[x]] == category.kind:
                i.delete()

    #   kategori silinecek
    category.delete()

    return redirect("/user/admin/categories/")