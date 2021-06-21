from django.urls import path
from extras import views

urlpatterns = [
    path('', views.index, name="index"),
    path('wraps/', views.extrasWrap, name="wraps"),
    path('atistirmaliklar/', views.extrasSnack, name="snacks"),
    path('makarnalar/', views.extrasMacaroni, name="macaroni"),
    path('icecekler/', views.extrasDrinks, name="drinks"),
    path('tatlilar/', views.extrasDesserts, name="desserts"),

    #admin
    path('admin/extras/',views.extras, name="extras"),
    path('admin/extras/add/',views.extraAdd, name="extraAdd"),
    path('admin/extras/edit/<int:id>',views.extraEdit, name="extraEdit"),
    path('admin/extras/delete/<int:id>',views.extraDelete, name="extraDelete"),
]
