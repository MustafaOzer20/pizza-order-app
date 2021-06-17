from os import name
from django.contrib import admin
from django.urls import path
from basket import views

app_name = "basket"

urlpatterns = [
    path('basketItems/', views.basketList, name="basketItems"),
    path('basketItems/delete/<int:id>', views.delete, name="removeItem"),
    path('basketItems/updatePiece/add/<int:id>', views.updateAddPiece, name="updateAddPiece"),
    path('basketItems/updatePiece/reduce/<int:id>', views.updateReducePiece, name="updateReducePiece"),

    #payment
    path('payment/', views.payment, name="payment")
]