from extras.models import Extra
from django import forms 

class ExtraForm(forms.ModelForm):
    class Meta:
        model = Extra
        fields = '__all__'