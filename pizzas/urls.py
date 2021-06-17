from os import name
from django.contrib import admin
from django.urls import path
from pizzas import views

urlpatterns = [
    #pizzas category
    path('', views.pizzas, name="pizzas"),
    path('cazip/', views.cazip, name="cazip"),
    path('special/', views.special, name="special"),
    path('bolmalzemeli/', views.bolmalzeme, name="bolmalzemeli"),
    path('gurme/', views.gurme, name="gurme"),

    #basket
    path('addtobasket/<int:id>', views.basket, name="basket")
]
