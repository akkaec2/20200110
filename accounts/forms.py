from django.contrib.auth.models import User 
from django.contrib.auth.forms import UserCreationForm 
from django.contrib.auth.forms import AuthenticationForm 
from django import forms
from .models import Post4
# from .models import Post2,Post1
from django.utils import timezone
import logging

CrossSection_CHOICES = (
    ('',''),
    ('下','下'),
    ('中','中'),
    ('上','上'),
)
#モデルの名前設定
model = Post4

logger = logging.getLogger('command')

# Create your views here.
class LoginForm(AuthenticationForm): 
    # logger = logging.getLogger('command')
    # logger.info('LoginForm')
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

#2019/12/4 16:45 csvの中身を読み取る方法を知るためのもの（出荷実績で実施）
class CSVUploadForm(forms.Form):
    file = forms.FileField(label='CSVファイル', help_text='※拡張子csvのファイルをアップロードしてください。')


#連番の入力値
class PailNumForm(forms.Form):
    # delivery_checker = forms.CharField(label="納品確認者")
    # serial_num = forms.CharField(label="連番")

    def save(self,serial_num):
        # deli_name                = self.cleaned_data.get('delivery_checker')
        # serial_num               = self.cleaned_data.get('serial_num')
        pail_num                 = model.objects.get(serial_num=serial_num)
        dt_now                   = timezone.datetime.now()
        pail_num.delivery_record = dt_now.strftime('%Y/%m/%d %H:%M')#納品実績に時刻を登録　←　秒数削除
        # pail_num.deliverer       = self.cleaned_data.get('delivery_checker')#納品確認者にテキストにある人名を登録
        pail_num.save()

class PailNumForm_con(forms.Form):
    # inspector = forms.CharField(label="検査者")
    # serial_num = forms.CharField(label="連番")

    def save(self,serial_num):
        # ins_name                     = self.cleaned_data.get('inspector')
        # serial_num                   = self.cleaned_data.get('serial_num')
        pail_num                     = model.objects.get(serial_num=serial_num)
        dt_now                       = timezone.datetime.now()
        pail_num.material_inspection = dt_now.strftime('%Y/%m/%d %H:%M')#材料検査に時刻を登録　←　秒数削除
        # pail_num.inspector           = self.cleaned_data.get('inspector')#検査者にテキストにある人名を登録
        pail_num.save()

class PailNumForm_cas(forms.Form):
    # caster        = forms.CharField(label="打設者")
    # serial_num    = forms.CharField(label="連番")
    pail_num      = forms.CharField(label="杭番号")
#     # cross_section = forms.CharField(label="断面")
#     cross_section = forms.ChoiceField(
#         label="断面",
#         widget=forms.Select,
#         choices=CrossSection_CHOICES,
#         required=False,
# )
    def save(self,serial_num,pail_num,cross_section):#(self,serial_num,pail_num,cross_section):
        pail_num1                      = model.objects.get(serial_num=serial_num)
        dt_now                         = timezone.datetime.now()
        pail_num1.start_casting        = dt_now.strftime('%Y/%m/%d %H:%M:%S')#打設時間に時刻を登録
        # pail_num1.start_casting        = dt_now.strftime('%Y-%m-%d %H:%M')#打設時間に時刻を登録　←　秒数削除
        # pail_num1.caster               = self.cleaned_data.get('caster')#打設者にテキストにある人名を登録
        # pail_num1.pail_num             = pail_num                         #杭番号に登録 inputで入力する用
        pail_num1.pail_num             = self.cleaned_data.get('pail_num')#杭番号に登録 　formから入力する用
        pail_num1.cross_section        = cross_section                      #断面に登録
        pail_num1.save()

class PailSearchForm(forms.Form):
    serial_num    = forms.CharField(label="連番",required=False)
    pail_num      = forms.CharField(label="杭番号",required=False)
    # cross_section = forms.CharField(label="断面",required=False)
    cross_section = forms.ChoiceField(
        label="断面",
        initial="",
        widget=forms.Select,
        choices=CrossSection_CHOICES,
        required=False,
    )

class PailCorrectForm(forms.Form):
    # serial_num    = forms.CharField(label="連番",required=False)

    def save(self,serial_num,pail_num,cross_section):
        pail_num1               = model.objects.get(serial_num=serial_num)
        dt_now                  = timezone.datetime.now()
        pail_num1.start_casting = dt_now.strftime('%Y/%m/%d %H:%M:%S')#打設時間に時刻を登録
        pail_num1.pail_num      = pail_num
        pail_num1.cross_section = cross_section
        pail_num1.save()

class ManagementCorrectForm(forms.Form):
    # serial_num    = forms.CharField(label="連番",required=False)

    def save(self,serial_num,pail_num,cross_section):
        pail_num1               = model.objects.get(serial_num=serial_num)
        dt_now                  = timezone.datetime.now()
        pail_num1.correction    = dt_now.strftime('%Y/%m/%d %H:%M')#打設時間に時刻を登録
        pail_num1.pail_num      = pail_num
        pail_num1.cross_section = cross_section
        pail_num1.save()


# PailSearchFormSet = forms.formset_factory(PailSearchForm,extra=1)

# 練習
class KakikomiForm(forms.Form):
     name = forms.CharField()
     email = forms.EmailField()
     body = forms.CharField() 


