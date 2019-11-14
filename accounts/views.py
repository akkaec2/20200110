from django.shortcuts import render, redirect 
from django.contrib.auth import login, authenticate 
from django.contrib.auth.models import User 
from django.views.generic import CreateView, TemplateView 
from .forms import UserCreateForm, LoginForm
from tkinter import messagebox

#確認用
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
        #アカウントを作成できない確認用20191113
        # else:
        #     messagebox.showerror('era-','アカウントを作成できません')

        return render(request, 'create.html', {'form': form,}) 

    def get(self, request, *args, **kwargs): 
        form = UserCreateForm(request.POST) 
        return  render(request, 'create.html', {'form': form,}) 

create_account = Create_Account.as_view() 

#ログイン後画面表示
# def main_operate(request):
#     # return HttpResponse("Hello, world.")
#     return render(request,'operate.html')

#ログイン後右側の画面（杭照合）
def collation(request):
    # f = TablerowForm(data = request.POST)
    return render(request,'collation.html')#,{'form1':f}

#ログイン後右側の画面（受入検査）
def confirm(request):
    return render(request,'confirm.html') 

#ログイン後右側の画面（打設位置＋杭）
def casting(request):
    return render(request,'casting.html')

#ログイン後右側の画面（進捗管理）
def management(request):
    return render(request,'management.html')