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

    

    #change
    path('change/username/', views.usernameChange, name="usernameChange"),
    path('change/email/', views.emailChange, name="emailChange"),
    path('change/password/', views.passwdChange, name="passwdChange"),
]
