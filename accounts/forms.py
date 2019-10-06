from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.forms import AuthenticationForm 
from django import forms


# Create your views here.
class LoginForm(AuthenticationForm): 
    def __init__(self, *args, **kwargs): 
       super().__init__(*args, **kwargs) 
       #htmlの表示を変更可能にします 
       self.fields['username'].widget.attrs['class'] = 'form-control' 
       self.fields['password'].widget.attrs['class'] = 'form-control' 

class UserCreateForm(UserCreationForm): 
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['username'].widget.attrs['class'] = 'form-control' 
        self.fields['password1'].widget.attrs['class'] = 'form-control' 
        self.fields['password2'].widget.attrs['class'] = 'form-control' 

    class Meta: 
       model = User 
       fields = ("username", "password1", "password2",) 

class PailNumForm(forms.Form):
    pail_num = forms.CharField(
        label='杭番号',
        # max_length=200,
        required = True,
        widget=forms.TextInput()
    )
    pail_detail_num = forms.CharField(
        label='杭詳細番号',
        # max_length=200,
        required = True,
        widget=forms.TextInput()
    )
