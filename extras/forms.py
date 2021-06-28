from pizzas.models import CategoryManagment
from extras.models import Extra
from django import forms 

class ExtraForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ExtraForm, self).__init__(*args, **kwargs)
        getCategory = CategoryManagment.objects.filter(kind="Ekstra")
        categoryNames = []
        for i in getCategory:
            temp = (i.name,i.name)
            categoryNames.append(temp)
        categoryNames = tuple(categoryNames)
        self.fields['category'] = forms.ChoiceField(
            choices=categoryNames
        )
    class Meta:
        model = Extra
        fields = '__all__'