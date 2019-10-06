# from django.shortcuts import render
from django.shortcuts import render, redirect 
from django.views import View 
from django.contrib.auth import login, authenticate 
from django.contrib.auth.models import User 
from django.views.generic import CreateView, TemplateView 
from .forms import UserCreateForm, LoginForm, PailNumForm
# from accounts.models import PailnumModel
from django.http import HttpResponse

pdict = {0:0}


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
            return render(request,'operate.html') #operate.html
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
 

#ログイン後右側の画面（杭番号明細紐づけ画面）
def pail_num_detail(request):
    f=PailNumForm(data=request.POST)
    if f.is_valid():
        a = f.cleaned_data.get('pail_num')
        b = f.cleaned_data.get('pail_detail_num')
        p_dict(a,b)
        return render(request,'ok.html')
    return render(request,'pail_num_detail.html',{'form1':f})


#ログイン後右側の画面（杭番号明細紐づけ画面）登録する
def p_dict(p_num,p_detail_num):
    pdict[p_num] = p_detail_num
    a = pdict
    return a

#ログイン後画面表示
def main_operate(request):
    # return HttpResponse("Hello, world.")
    return render(request,'operate.html')

#ログイン後右側の画面（出荷情報受信画面）
def deli_info(request):
    return render(request,'deli_info.html')

#ログイン後右側の画面（照合画面）
def collation(request):
    return render(request,'collation.html')
#ログイン後右側の画面（打設確認画面）
def casting(request):
    return render(request,'casting.html')

#ログイン後右側の画面（杭番号明細紐づけ画面登録後）
def ok(request):
    return render(request,'ok.html')

#ログイン後右側の画面（確認画面）
def confirm(request):
    pd = p_dict
    d = {
        'pd':pd
    }
    return render(request,'confirm.html',d) 

# class Pail_num_detail(CreateView):
#     def post(self, request, *args, **kwargs):
#         f = PailNumForm(data=request.POST)
#         if f.is_vaild():
#             f.save() 
#             pail_num = f.cleaned_dataget["pail_num"]
#             pail_detail_num = f.cleaned_data.get['pail_detail_num']
#             # https://qiita.com/peijipe/items/009fc487505dfdb03a8d
#             return render(request,'ok.html')
#         return render(request, 'pail_num_detail.html', {'form1': f})
#     def get(self, request, *args, **kwargs):
#         f = PailNumForm(data=request.POST)
#         return render(request,'pail_num_detail.html',{'form1': f})

# pail_num_detail = Pail_num_detail.as_view()



# class P_dict(PailNumForm):
#     def p_dict(request,pail_num,pail_detail_num):
#         a = pail_num
#         b = pail_detail_num
#         pail_dict[a] = b
#         return render(request,'confirm.html')
#             #    f1 = f['pail_num']