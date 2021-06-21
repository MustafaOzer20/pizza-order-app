from django.urls import path
from pizzas import views

urlpatterns = [
    #pizzas category
    path('', views.pizzas, name="pizzas"),
    path('cazip/', views.cazip, name="cazip"),
    path('special/', views.special, name="special"),
    path('bolmalzemeli/', views.bolmalzeme, name="bolmalzemeli"),
    path('gurme/', views.gurme, name="gurme"),

    #admin
    path('admin/products/', views.products, name="products"),
    path('admin/products/edit/<int:id>', views.productsEdit, name="productsEdit"),
    path('admin/products/add/', views.productsAdd, name="productsAdd"),
    path('admin/products/delete/<int:id>', views.productsDelete, name="productsDelete"),
]
