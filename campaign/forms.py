from campaign.models import Campaign
from django import forms 

class CampaignForm(forms.ModelForm):
    class Meta:
        model = Campaign
        fields = '__all__'