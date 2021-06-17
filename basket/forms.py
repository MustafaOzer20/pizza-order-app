from django import forms

SIZE_CHOICES = (
    ("1", "Küçük Boy"),
    ("2", "Orta Boy"),
    ("3", "Büyük Boy"),
)


class BasketForm(forms.Form):
    piece = forms.IntegerField(min_value=1, max_value=10, label="Adet")
    size = forms.ChoiceField(choices=SIZE_CHOICES, label="Boy", help_text="Küçük Boy -15TL ----- Orta Boy -10TL")


PAYMETHOD_CHOICES = (
    ("1", "Kapıda Ödeme(Nakit)"),
    ("2", "Kapıda Ödeme(Kart)"),
    ("3", "Online Ödeme"),
)
class OrderForm(forms.Form):
    adress = forms.CharField(max_length=300, label="Adres Bilgisi")
    phone_number = forms.CharField(max_length=10, label="Telefon Numarası",help_text="10 haneli telefon numarası giriniz: (5XX)XXXXXXX")
    user_note = forms.CharField(min_length=0,max_length=200,required=False, empty_value="-", label="Kullanıcı Notu", help_text="Siparişle ilgili ek bilgi(isteğe bağlı)")
    payment_method = forms.ChoiceField(choices=PAYMETHOD_CHOICES, label="Ödeme Yöntemi")


STATUS_CHOICES = (
    ("1", "Hazırlanıyor"),
    ("2", "Yolda"),
    ("3", "Teslim Edildi"),
)
class AdminForm(forms.Form):
    orderId = forms.IntegerField(min_value=1)
    status = forms.ChoiceField(choices=STATUS_CHOICES, label="Durum")
