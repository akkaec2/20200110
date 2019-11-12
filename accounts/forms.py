from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.forms import AuthenticationForm 
from django import forms


# Create your views here.
class LoginForm(AuthenticationForm): 
    def __init__(self, *args, **kwargs): 
       super().__init__(*args, **kwargs) 
       #htmlの表示を変更可能にします 
       self.fields['username'].widget.attrs['cols'] = 100 #大きさ変更できるようにする
       self.fields['password'].widget.attrs['rows'] = 100

class UserCreateForm(UserCreationForm): 
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['username'].widget.attrs['class'] = 'form-control' 
        self.fields['password1'].widget.attrs['class'] = 'form-control' 
        self.fields['password2'].widget.attrs['class'] = 'form-control' 

    class Meta: 
       model = User 
       fields = ("username", "password1", "password2",) 


#csvをアップロードする仕組み
class UploadFileForm(forms.Form):
    #formのname属性が'file'になる
     file = forms.FileField(required=True, label='CSVファイル')