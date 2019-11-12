from django.shortcuts import render, redirect 
from django.views import View 
from django.contrib.auth import login, authenticate 
from django.contrib.auth.models import User 
from django.views.generic import CreateView, TemplateView 
from .forms import UserCreateForm, LoginForm
from django.http import HttpResponse
from .forms import UploadFileForm
import os, csv

#Webサーバのファイルの指定　　のはず．．．
#今回は「施工現場csv受信」にした
# UPLOAD_DIR='http://10.82.90.69/%E5%BB%BA%E6%9D%90csv/%E6%96%BD%E5%B7%A5%E7%8F%BE%E5%A0%B4csv%E5%8F%97%E4%BF%A1/'


# Create your views here.

#ログイン 
class Account_login(TemplateView): 
    template_name = 'login.html'
    def post(self, request, *arg, **kwargs): 
        form = LoginForm(data=request.POST) 
        if form.is_valid(): 
            username = form.cleaned_data.get('username') 
            user = User.objects.get(username=username) 
            login(request, user) 
            return render(request,'collation.html') #operate.html →　collation.html
        return render(request, 'login.html', {'form': form,}) #変更点　2019/9/26'login.html'→'index.html'へ
    def get(self, request, *args, **kwargs): 
        form = LoginForm(request.POST) 
        return render(request, 'login.html', {'form': form,}) #変更点　2019/9/26'login.html'→'index.html'へ
 
account_login = Account_login.as_view() 

#アカウント作成 
class Create_Account(CreateView): 
    def post(self, request, *args, **kwargs): 
        form = UserCreateForm(data=request.POST) 
        if form.is_valid(): 
            form.save() 
            #フォームから'username'を読み取る 
            username = form.cleaned_data.get('username') 
            #フォームから'password1'を読み取る 
            password = form.cleaned_data.get('password1') 
            #フォームに入力された'username', 'password1'が一致する会員をDBから探し，userに代入 
            user = authenticate(username=username, password=password) 
            login(request, user) 
            return redirect('/') 
        return render(request, 'create.html', {'form': form,}) 

    def get(self, request, *args, **kwargs): 
        form = UserCreateForm(request.POST) 
        return  render(request, 'create.html', {'form': form,}) 

create_account = Create_Account.as_view() 
 
#ログイン後画面表示
def main_operate(request):
    # return HttpResponse("Hello, world.")
    return render(request,'operate.html')

#ログイン後右側の画面（照合画面）
def collation(request):
    # f = TablerowForm(data = request.POST)
    return render(request,'collation.html')#,{'form1':f}

#ログイン後右側の画面（打設確認画面）
def casting(request):
    return render(request,'casting.html')

#ログイン後右側の画面（確認画面）
def confirm(request):
    return render(request,'confirm.html') 




#杭照合でのファイル選択
def CsvUpload(request):
    if request.method == 'POST':
        #POST
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            # file is saved. by binary
            f = request.FILES['file']                       #ファイルデータを request.FILES で 受け取り
            path = os.path.join(UPLOAD_DIR, f.name)         #ファイルパスとファイル名を統合したパス
            with open(path) as csvfile:
                l = csvfile.readlines()
            return redirect('/')
    
    else:
        #GET
        form = UploadFileForm()

        return render(request,'login.html',{'form': form})         #まだGETができていないので出来ていないときはLOGIN画面に飛んでもらう

