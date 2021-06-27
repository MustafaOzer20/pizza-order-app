from os import name
from django.urls import path
from extras import views

urlpatterns = [
    path('', views.index, name="index"),
    path('<str:name>', views.categoryExtra, name="category"),
    
    #admin
    path('admin/extras/',views.extras, name="extras"),
    path('admin/extras/add/',views.extraAdd, name="extraAdd"),
    path('admin/extras/edit/<int:id>',views.extraEdit, name="extraEdit"),
    path('admin/extras/delete/<int:id>',views.extraDelete, name="extraDelete"),
]
