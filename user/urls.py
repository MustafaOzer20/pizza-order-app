from os import name
from django.urls import path
from user import views

app_name = "user"

urlpatterns = [
    #user operation
    path('register/', views.register, name="register"),
    path('login/', views.loginUser, name="login"),
    path('logout/', views.logoutUser, name="logout"),

    #profile
    path('myaccount/', views.profile, name="profile"),
    path('myaccount/siparislerim/', views.myOrders, name="myorders"),

    #admin
    path('admin/orders/', views.orders, name="orders"),
    path('admin/dashboard/', views.adminDashboard, name="dashboard"),
    path('admin/categories/',views.listCategories,name="categories"),
    path('admin/categories/add/',views.addCategory,name="categoryAdd"),
    path('admin/categories/edit/<int:id>',views.editCategory,name="categoryEdit"),
    path('admin/categories/delete/<int:id>',views.deleteCategory,name="categoryDelete"),

    #emailverify
    path('activate/<str:uidb64>/<str:token>',views.activate, name="activate"),

    #forgot password
    path('forget/password/',views.forgetPassword, name="forgot"),
    path('forget/password/<str:uidb64>/<str:token>',views.changePasswdtoForget, name="changeForgot"),

    #change
    path('change/username/', views.usernameChange, name="usernameChange"),
    path('change/email/', views.emailChange, name="emailChange"),
    path('change/email/<str:uidb64>/<str:token>',views.emailChangeToken, name="emailChangeToken"),
    path('change/password/', views.passwdChange, name="passwdChange"),
]
