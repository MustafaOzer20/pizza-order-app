from django.db.models import fields
from pizzas.models import CategoryManagment, Pizza
from django import forms 


class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ('title','contents','price','imageUrl','category')


class CategoryForm(forms.ModelForm):
    class Meta:
        model = CategoryManagment
        fields = ('__all__')

class CategoryFormWithoutKind(forms.ModelForm):
    class Meta:
        model = CategoryManagment
        fields = ('name',)