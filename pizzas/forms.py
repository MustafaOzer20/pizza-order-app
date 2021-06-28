from pizzas.models import CategoryManagment, Pizza
from django import forms 


class PizzaForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PizzaForm, self).__init__(*args, **kwargs)
        getCategory = CategoryManagment.objects.filter(kind="Pizza")
        categoryNames = []
        for i in getCategory:
            temp = (i.name,i.name)
            categoryNames.append(temp)
        categoryNames = tuple(categoryNames)
        self.fields['category'] = forms.ChoiceField(
            choices=categoryNames
        )
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