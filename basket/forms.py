from django import forms
from django.forms.forms import Form

SIZE_CHOICES = (
    ("1", "Küçük Boy"),
    ("2", "Orta Boy"),
    ("3", "Büyük Boy"),
)


class BasketForm(forms.Form):
    piece = forms.IntegerField(min_value=1, max_value=20, label="Adet")
    size = forms.ChoiceField(choices=SIZE_CHOICES, label="Boy", help_text="Küçük Boy -15TL ----- Orta Boy -10TL")

class CampaignBasketForm(forms.Form):
    piece = forms.IntegerField(min_value=1, max_value=20, label="Adet")


PAYMETHOD_CHOICES = (
    ("Kapıda Ödeme(Nakit)", "Kapıda Ödeme(Nakit)"),
    ("Kapıda Ödeme(Kart)", "Kapıda Ödeme(Kart)"),
    ("Online Ödeme", "Online Ödeme"),
)
class OrderForm(forms.Form):
    adress = forms.CharField(max_length=300, label="Adres Bilgisi")
    phone_number = forms.CharField(max_length=10, label="Telefon Numarası",help_text="10 haneli telefon numarası giriniz: (5XX)XXXXXXX")
    user_note = forms.CharField(min_length=0,max_length=200,required=False, empty_value="-", label="Kullanıcı Notu", help_text="Siparişle ilgili ek bilgi(isteğe bağlı)")


STATUS_CHOICES = (
    ("1", "Hazırlanıyor"),
    ("2", "Yolda"),
    ("3", "Teslim Edildi"),
)
class AdminForm(forms.Form):
    orderId = forms.IntegerField(min_value=1)
    status = forms.ChoiceField(choices=STATUS_CHOICES, label="Durum")


class OrderWithPaymentForm(forms.Form):
    adress = forms.CharField(max_length=300, label="Adres Bilgisi")
    phone_number = forms.CharField(max_length=10, label="Telefon Numarası",help_text="10 haneli telefon numarası giriniz: (5XX)XXXXXXX")
    user_note = forms.CharField(min_length=0,max_length=200,required=False, empty_value="-", label="Kullanıcı Notu", help_text="Siparişle ilgili ek bilgi(isteğe bağlı)")
    full_name = forms.CharField(min_length=6, max_length=50, label="Kart Üzerindeki İsim", help_text="Kart sahibinin ismi ve soyismi")
    cardNumber = forms.CharField(min_length=16, max_length=16, label="Kart Numarası", help_text="Örnek: 1234567891234567")
    cvv = forms.IntegerField(min_value=100, max_value=999, label="CVV", help_text="Kartınızın arka yüzündeki CVV kodunu girin.")
    validTHRU = forms.CharField(help_text="mm/yy, olarak yazın", label="Son Kullanma Tarihi")

class PayMethodForm(forms.Form):
    payment_method = forms.ChoiceField(choices=PAYMETHOD_CHOICES, label="Ödeme Yöntemi")