from os import name
from django.urls import path
from campaign import views

urlpatterns = [
    path('', views.index, name="index"),
    path('<str:name>/', views.categoryCampaign, name="category"),
    

    # admin
    path('admin/campaign/',views.campaign, name="campaign"),
    path('admin/campaign/add/',views.campaignAdd, name="campaignAdd"),
    path('admin/campaign/edit/<int:id>',views.campaignEdit, name="campaignEdit"),
    path('admin/campaign/delete/<int:id>',views.campaignDelete, name="campaignDelete"),
]
