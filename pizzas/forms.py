from pizzas.models import Pizza
from django import forms 

class PizzaForm(forms.ModelForm):
    class Meta:
        model = Pizza
        fields = ('title','contents','price','imageUrl','category')