from pizzas.models import CategoryManagment
from campaign.models import Campaign
from django import forms 

class CampaignForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CampaignForm, self).__init__(*args, **kwargs)
        getCategory = CategoryManagment.objects.filter(kind="Kampanya")
        categoryNames = []
        for i in getCategory:
            temp = (i.name,i.name)
            categoryNames.append(temp)
        categoryNames = tuple(categoryNames)
        self.fields['category'] = forms.ChoiceField(
            choices=categoryNames
        )
    class Meta:
        model = Campaign
        fields = '__all__'