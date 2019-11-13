from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.forms import AuthenticationForm 


# Create your views here.
class LoginForm(AuthenticationForm): 
    def __init__(self, *args, **kwargs): 
       super().__init__(*args, **kwargs) 
       #htmlの表示を変更可能にします 
       self.fields['username'].widget.attrs['cols'] ='form-control' #大きさ変更できるようにする 20191113    100としていた
       self.fields['password'].widget.attrs['rows'] = 'form-control'

class UserCreateForm(UserCreationForm): 
    def __init__(self, *args, **kwargs): 
        super().__init__(*args, **kwargs) 
        self.fields['username'].widget.attrs['class'] = 'form-control' 
        self.fields['password1'].widget.attrs['class'] = 'form-control' 
        self.fields['password2'].widget.attrs['class'] = 'form-control' 

    class Meta: 
       model = User 
       fields = ("username", "password1", "password2",) 

