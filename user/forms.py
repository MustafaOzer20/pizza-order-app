from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label="Kullanıcı Adı")
    password = forms.CharField(label="Parola", widget=forms.PasswordInput)


class ForgetPasswdForm(forms.Form):
    email = forms.EmailField(max_length=254)
    def clean(self):
        email = self.cleaned_data.get("email")
        values = {"email":email}
        return values


class ChangeForgotPasswd(forms.Form):
    password = forms.CharField(min_length=8, max_length=20,label="Parola", widget=forms.PasswordInput)
    confirm = forms.CharField(min_length=8, max_length=20, label="Parolayı Doğrula", widget=forms.PasswordInput)
    def clean(self):
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")
        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar Eşleşmiyor")

        values = {
            "password": password,
        }
        return values

class RegisterForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=20,label="Kullanıcı Adı")
    first_name = forms.CharField(min_length=3,max_length=20,label="İsim")
    last_name = forms.CharField(min_length=2, max_length=20, label="Soyisim")
    email = forms.EmailField(max_length=254)
    password = forms.CharField(min_length=8, max_length=20,label="Parola", widget=forms.PasswordInput)
    confirm = forms.CharField(min_length=8, max_length=20, label="Parolayı Doğrula", widget=forms.PasswordInput)
    
    def clean(self):
        username = self.cleaned_data.get("username")
        first_name = self.cleaned_data.get("first_name")
        last_name = self.cleaned_data.get("last_name")
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")
        
        if password and confirm and password != confirm:
            raise forms.ValidationError("Parolalar Eşleşmiyor")
        
        values = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "password": password,
        }
        return values



class changeEmailForm(forms.Form):
    email = forms.EmailField(max_length=254, label="Yeni Email")
    password = forms.CharField(min_length=8, max_length=20,label="Parola", widget=forms.PasswordInput)
    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        values = {
            "password": password,
            "email": email,
        }
        return values

class changePasswdForm(forms.Form):
    password = forms.CharField(min_length=8, max_length=20,label="Eski Parola", widget=forms.PasswordInput)
    newPasswd = forms.CharField(min_length=8, max_length=20,label="Yeni Parola", widget=forms.PasswordInput)
    confirm = forms.CharField(min_length=8, max_length=20, label="Yeni Parolayı Doğrula", widget=forms.PasswordInput)
    def clean(self):
        password = self.cleaned_data.get("password")
        newPasswd = self.cleaned_data.get("newPasswd")
        confirm = self.cleaned_data.get("confirm")
        if newPasswd and confirm and newPasswd != confirm:
            raise forms.ValidationError("Parolalar Eşleşmiyor")

        values = {
            "password": password,
            "newPasswd": newPasswd,
        }
        return values

class changeUsernameForm(forms.Form):
    username = forms.CharField(min_length=3, max_length=20,label="Yeni Kullanıcı Adı")
    password = forms.CharField(min_length=8, max_length=20,label="Parola", widget=forms.PasswordInput)
    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        values = {
            "password": password,
            "username": username,
        }
        return values


RATINGS_CHOICES =(
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("4", "4"),
    ("5", "5"),
)
class OrderRatings(forms.Form):
    comments = forms.CharField(label="Yorum", min_length=5,max_length=260)
    rating = forms.ChoiceField(label="Değerlendir",choices=RATINGS_CHOICES)