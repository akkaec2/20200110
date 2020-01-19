from django.shortcuts import render, redirect 
from django.contrib.auth import login, authenticate 
from django.contrib.auth.models import User 
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import UserCreateForm, LoginForm,KakikomiForm,CSVUploadForm,PailNumForm,PailNumForm_con,PailNumForm_cas,PailSearchForm,PailCorrectForm,ManagementCorrectForm
# from .forms import UserCreateForm, LoginForm,KakikomiForm,CSVUploadForm,PailNumForm,PailNumForm_con,PailNumForm_cas,PailNumForm_num
from .models import Post4
# from .models import sample2,sample3,sample4,FileNameModel,Post1,Post2,Post4
from io import TextIOWrapper, StringIO
from django.template.context_processors import csrf
from django.conf import settings
from django.urls import reverse_lazy
from django.views import generic
from django.utils import timezone
from django.db.models import Q
from django.db.models import CharField, Case, When, Value
import csv
import sys, os
import urllib
import io
import logging
import json

# logger = logging.getLogger('development') 
logger = logging.getLogger('command')


#モデルの名前設定
model = Post4

#ログイン
class Account_login(TemplateView): 
    template_name = 'login.html'
    def post(self, request, *arg, **kwargs): 
        form = LoginForm(data=request.POST) 
        if form.is_valid(): 
            username = form.cleaned_data.get('username') 
            user = User.objects.get(username=username) 
            login(request, user) 
            return render(request,'operate.html') #operate.html ←　collation.html　ログイン後のURLで/collation/とできなかったため一つoperateを挟むようにした
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

# 2019/12/5 8:25csvの中身を読み取る方法を知るためのもの（役職で実施）
#listviewにデータのリストを表示させるためのメソッドや属性が入っている．リストを表示するときはListViewを使うと便利
class PostImport(generic.ListView,generic.FormView):
    """テーブルの登録(csvアップロード)"""
    #クエリセットを作成してみた
    # queryset = model.objects.all()
    #PostImportクラスが呼び出されたときに使うDBtableを指定する
    model = model
    #djangoでは、template_nameを指定することで、このクラス（PostImport）呼び出されたときにブラウザに表示するhtmlファイルを指定することができるようになります.
    # template_name = 'collation.html'
    template_name = 'management.html'
    success_url = reverse_lazy('collation')
    form_class = CSVUploadForm
    def form_valid(self, form):
        """postされたCSVファイルを読み込み、テーブルに登録します"""#DBへの保存であってDBの値を取得しているわけではない
        csvfile = io.TextIOWrapper(form.cleaned_data['file'], encoding='utf-8_sig')
        reader = csv.reader(csvfile)
        for row in reader:
            """テーブルをコード(primary key)で検索します"""
            #テーブルによって変更する点
            post, created = model.objects.get_or_create(serial_num=row[0])
            post.save()
        return super().form_valid(form)

#collationの所
def collation(request):
    """request.postの値を確認して値が入っていなければ，form入力用の最初にユーザが見る画面を送るようにする"""
    if request.method == "POST":
        logger = logging.getLogger('command')
        Uploadform  = CSVUploadForm
        Pailnumform = PailNumForm(data = request.POST) 
        pail_data = model.objects.filter(delivery_record="",deliverer="").order_by('serial_num')
        # if Pailnumform.is_valid():
        # serial_num = Pailnumform.cleaned_data.get('serial_num')
        serial_num = request.POST.get('serial_num')
        #入力値(serial_num)がDB内の列 (serial_num)にあるかをカウントすることで確認
        # PostImportでserial_numは被らないようにしているので個数は1,0になるはず           
        pnum = model.objects.filter(serial_num=serial_num).count()
        #杭番号を読込んでいないとき
        if not request.POST.get('serial_num'):
            message = '杭を読込んでください'
            d = {'Uploadform':Uploadform,'Pailnumform':Pailnumform,'pail_data':pail_data,'message':message}
            return render(request,'collation.html',d)
        #入力値がDB内にないとき
        if pnum == 0:
            message = '読込んだ杭は出荷実績に含まれていません'
            d = {'Uploadform':Uploadform,'Pailnumform':Pailnumform,'pail_data':pail_data,'message':message}
            return render(request,'collation.html',d)
        #＝＝＝＝＝＝＝＝＝＝＝＝＝出荷実績に対応した納品実績が埋まっていないとき（データをsaveするとき）＝＝＝＝＝＝＝＝＝＝＝＝＝
        if model.objects.filter(serial_num=serial_num,delivery_record=""):
            Pailnumform.save(serial_num)
            d = {'Uploadform':Uploadform,'Pailnumform':Pailnumform,'pail_data':pail_data}
            return render(request,'collation.html',d)
        #出荷実績に対応した納品実績が埋まっているものを再度読込むと以下に入る
        else:
            message = '読込んだ杭は既に読込まれています'
            d = {'Uploadform':Uploadform,'Pailnumform':Pailnumform,'pail_data':pail_data,'message':message}
            return render(request,'collation.html',d)
    else:
        logger = logging.getLogger('command')
        Uploadform  = CSVUploadForm
        Pailnumform = PailNumForm(request.POST)
        # pail_data = model.objects.all().order_by('serial_num')
        pail_data = model.objects.filter(delivery_record="",deliverer="").order_by('serial_num')

        # key = msvcrt.getch()
        # i = 0
        d = {'Uploadform':Uploadform,'Pailnumform':Pailnumform,'pail_data':pail_data}
        
    return render(request,'collation.html',d)


#ログイン後右側の画面（受入検査）ここにform使用時の物を残す
def confirm(request):
    """request.postの値を確認して値が入っていなければ，form入力用の最初にユーザが見る画面を送るようにする"""
    if request.method == "POST":
        logger = logging.getLogger('command')
        Pailnumform_con = PailNumForm_con(data = request.POST) 
        # pail_data = model.objects.all().order_by('serial_num')
        pail_data = model.objects.filter(material_inspection="",inspector="").order_by('serial_num')

        # if Pailnumform_con.is_valid():
        serial_num = request.POST.get('serial_num')
        pnum = model.objects.filter(serial_num=serial_num).count()
        #連番を入力せずにボタンを押した場合
        if not request.POST.get('serial_num'):
            message = '杭を読込んでください'
            d = {'Pailnumform_con':Pailnumform_con,'pail_data':pail_data,'message':message}
            return render(request,'confirm.html',d)
        #入力値がDB内にないとき
        if pnum == 0:
            message = '読込んだ杭は出荷実績に含まれていません'
            d = {'Pailnumform_con':Pailnumform_con,'pail_data':pail_data,'message':message}
            return render(request,'confirm.html',d)
        #納品実績の時間が埋まっていない　→　納品確認を終えていないとき
        if model.objects.filter(serial_num=serial_num,delivery_record=""):
            message = 'この杭は納品確認を終えていません\n納品確認を実施してください'
            d = {'Pailnumform_con':Pailnumform_con,'pail_data':pail_data,'message':message,}
            return render(request,'confirm.html',d)
        #＝＝＝＝＝＝＝＝＝＝＝＝＝出荷実績に対応した材料検査が埋まっていないとき（データをsaveするとき）＝＝＝＝＝＝＝＝＝＝＝＝＝
        if model.objects.filter(serial_num=serial_num,material_inspection=""):
            Pailnumform_con.save(serial_num)
            d = {'Pailnumform_con':Pailnumform_con,'pail_data':pail_data}
            return render(request,'confirm.html',d)
        else:
            message = '読込んだ杭は既に読込まれています'
            d = {'Pailnumform_con':Pailnumform_con,'pail_data':pail_data,'message':message,}
            return render(request,'confirm.html',d)
    else:
        Pailnumform_con = PailNumForm_con(request.POST)
        # pail_data = model.objects.all().order_by('serial_num')
        pail_data = model.objects.filter(material_inspection="",inspector="").order_by('serial_num')
        d = {'Pailnumform_con':Pailnumform_con,'pail_data':pail_data}
    return render(request,'confirm.html',d)


#ログイン後右側の画面（打設位置＋杭）
def casting(request):
    logger = logging.getLogger('command')
    if request.method == "POST":
        pailnumform_cas = PailNumForm_cas(data = request.POST) 
        # pail_data = model.objects.all().order_by('serial_num')
        pail_data = model.objects.filter(start_casting="",caster="").order_by('serial_num')
        if pailnumform_cas.is_valid():
            pail_num      = pailnumform_cas.cleaned_data.get("pail_num")
            serial_num    = request.POST.get('serial_num')
            # pail_num      = request.POST.get('pail_num')
            cross_section = request.POST.get('cross_section')
            pnum = model.objects.filter(serial_num=serial_num).count()
            # #杭番号を入力していないとき
            # if not request.POST.get('pail_num'):
            #     message = '杭番号を入力してください'
            #     d = {'pailnumform_cas':pailnumform_cas,'pail_data':pail_data,'message':message,}
            #     return render(request,'casting.html',d)
            # #断面を選択していないとき
            # if not request.POST.get('cross_section'):
            #     message = '断面を選択してください'
            #     d = {'pailnumform_cas':pailnumform_cas,'pail_data':pail_data,'message':message}
            #     return render(request,'casting.html',d)
            #連番を入力せずにボタンを押した場合
            if not request.POST.get('serial_num'):
                message = '杭を読込んでください'
                d = {'pailnumform_cas':pailnumform_cas,'pail_data':pail_data,'message':message}
                return render(request,'casting.html',d)
            #断面を選択せずにボタンを押した場合
            if not request.POST.get('cross_section'):
                message = '断面を選択してください'
                d = {'pailnumform_cas':pailnumform_cas,'pail_data':pail_data,'message':message}
                return render(request,'casting.html',d)
            #入力値がDB内にないとき
            if pnum == 0:
                message = '読込んだ杭は出荷実績に含まれていません'
                d = {'pailnumform_cas':pailnumform_cas,'pail_data':pail_data,'message':message}
                return render(request,'casting.html',d)
            #納品実績の時間が埋まっていない　→　納品確認を終えていないとき
            if model.objects.filter(serial_num=serial_num,delivery_record=""):
                message = 'この杭は納品確認を終えていません\n納品確認を実施してください'
                d = {'pailnumform_cas':pailnumform_cas,'pail_data':pail_data,'message':message}
                return render(request,'casting.html',d)

            #杭番号と断面が既に登録されている場合（ある連番にその杭番号と断面のペアが与えられているとき）
            if model.objects.filter(pail_num=pail_num,cross_section=cross_section):
                if cross_section == "中":
                    pass
                else:
                    # d_message = '入力した杭番号と断面は既に登録されています'
                    d_message = '入力した情報は既に登録されています'
                    flag = {'serial_num':serial_num,'pail_num':pail_num,'cross_section':cross_section,'c':'杭番号・断面'}
                    logger.info(flag['serial_num'])
                    logger.info(flag['pail_num'])
                    logger.info(flag['cross_section'])
                    d = {'pailnumform_cas':pailnumform_cas,'pail_data':pail_data,'d_message':d_message,'flag':json.dumps(flag)}
                    return render(request,'casting.html',d)

            #＝＝＝＝＝＝＝＝＝＝＝＝＝出荷実績に対応した打設時刻が埋まっていないとき（まだDBに登録されていないとき）＝＝＝＝＝＝＝＝＝＝＝＝＝
            if model.objects.filter(serial_num=serial_num, start_casting=""):
                pailnumform_cas.save(serial_num,pail_num,cross_section)
                # pailnumform_cas.save(serial_num,cross_section)
                d = {'pailnumform_cas':pailnumform_cas,'pail_data':pail_data,}
                return render(request,'casting.html',d)

            #＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

            #★★ここをダイアログにする必要がある★★
            #杭番号と断面の入力情報の関係なしに，連番が登録されている場合　←　ここに行くことはないと考えられる
            else:
                d_message = '読込んだ杭は既に読込まれています'
                flag = {'serial_num':serial_num,'pail_num':pail_num,'cross_section':cross_section}
                logger.info(flag['serial_num'])
                logger.info(flag['pail_num'])
                logger.info(flag['cross_section'])
                # logger.info(flag['flag'])
                d = {'pailnumform_cas':pailnumform_cas,'pail_data':pail_data,'d_message':d_message,'flag':json.dumps(flag)}
                return render(request,'casting.html',d)
    else:
        pailnumform_cas = PailNumForm_cas(request.POST) 
        # pail_data = model.objects.all().order_by('serial_num')
        # pail_data = model.objects.filter(start_casting="",caster="").order_by('start_casting')
        pail_data = model.objects.filter(start_casting="",caster="").order_by('serial_num')
        d = {'pailnumform_cas':pailnumform_cas,'pail_data':pail_data}
    return render(request,'casting.html',d)

#ログイン後右側の画面（進捗管理)
class ManagementView(LoginRequiredMixin, generic.ListView):
    model = model
    template_name = 'management.html'
    # context_object_name = 'pail_data'
    
    def post(self, request, *args, **kwargs): 
        form_value = {
            'serial_num'    :self.request.POST.get('serial_num', None), 
            'pail_num'      :self.request.POST.get('pail_num', None), 
            'cross_section' :self.request.POST.get('cross_section', None), 
        }
        request.session['form_value'] = form_value
        # 検索時にページネーションに関連したエラーを防ぐ 
        # self.request.GET = self.request.GET.copy() 
        # self.request.GET.clear() 
        return self.get(request, *args, **kwargs) 

    # def post(self, request, *args, **kwargs): 
    #     pailsearchform = PailSearchForm(data = request.POST)
    #     m_serial_num = request.POST.get('m_serial_num')
    #     #修正機能の追加
    #     if m_serial_num:
    #         m_pail_num      = request.POST.get('m_pail_num')
    #         m_cross_section = request.POST.get('m_cross_section')
    #         managementcorrectform = ManagementCorrectForm(data = request.POST)
    #         # pail_data = model.objects.filter(start_casting="",caster="").order_by('serial_num')
    #         pail_data = model.objects.annotate(
    #             blank = Case(
    #                 When(start_casting = '', then = Value(1)),
    #                 default = Value(2),
    #                 output_field = CharField()
    #             )
    #         ).order_by('blank','-start_casting','serial_num')
    #         managementcorrectform.save(m_serial_num,m_pail_num,m_cross_section)
    #         d = {'pailsearchform':pailsearchform,'managementcorrectform':managementcorrectform,'pail_data':pail_data,}
    #         return render(request,'management.html',d)

    #     #検索機能の場合
    #     else:
    #         form_value = {
    #             'serial_num'    :self.request.POST.get('serial_num', None), 
    #             'pail_num'      :self.request.POST.get('pail_num', None), 
    #             'cross_section' :self.request.POST.get('cross_section', None), 
    #         }
    #         request.session['form_value'] = form_value
    #         # 検索時にページネーションに関連したエラーを防ぐ 
    #         # self.request.GET = self.request.GET.copy() 
    #         # self.request.GET.clear() 
    #         return self.get(request, *args, **kwargs) 


    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        # sessionに値がある場合、その値をセットする。（ページングしてもform値が変わらないように
        serial_num    = ''
        pail_num      = ''
        cross_section = ''
        if 'form_value' in self.request.session:
            form_value    = self.request.session['form_value']
            serial_num    = form_value['serial_num']
            pail_num      = form_value['pail_num']
            cross_section = form_value['cross_section']

        default_data = {
            'serial_num'    :serial_num,
            'pail_num'      :pail_num,
            'cross_section' :cross_section,
        }

        test_form = PailSearchForm(initial=default_data) # 検索フォーム
        context['test_form'] = test_form

        return context

    def get_queryset(self):
        # sessionに値がある場合、その値でクエリ発行する。
        if 'form_value' in self.request.session:
            form_value    = self.request.session['form_value']
            serial_num    = form_value['serial_num']
            pail_num      = form_value['pail_num']
            cross_section = form_value['cross_section']

            # 検索条件
            condition_serial_num    = Q()
            condition_pail_num      = Q()
            condition_cross_section = Q()

            if len(serial_num) != 0 and serial_num[0]:
                condition_serial_num = Q(serial_num__contains=serial_num)
            if len(pail_num) != 0 and pail_num[0]:
                condition_pail_num = Q(pail_num__contains = pail_num)
            if len(cross_section) != 0 and cross_section[0]:
                condition_cross_section = Q(cross_section__contains = cross_section)
            
            return model.objects.select_related().filter(condition_serial_num & condition_pail_num & condition_cross_section).annotate(
                blank = Case(
                    When(start_casting = '', then = Value(1)),
                    default = Value(2),
                    output_field = CharField()
                )
            ).order_by('blank','-start_casting','serial_num')

        else:
            return model.objects.none()

    def managementcorrectview(self):
        return render(request,'casting.html',d)

managementview = ManagementView.as_view() 

#「打設」で修正を加えるView
def pailcorrectview(request):
    # jsondata  = request.POST['flag_return']
    # jsondatas = json.loads(jsondata)
    # logger = logging.getLogger('command')
    pailcorrectform    = PailCorrectForm(data = request.POST) 
    pailnumform_cas    = PailNumForm_cas(data = request.POST) 
    # object_list        = model.objects.filter(start_casting="",caster="").order_by('serial_num')
    # if pailnumform_cas.is_valid():
    # serial_num    = request.POST.get('serial_num')
    serial_num     = request.GET['flag_serial_num']
    pail_num       = request.GET['flag_pail_num']
    cross_section  = request.GET['flag_cross_section']
    pailcorrectform.save(serial_num,pail_num,cross_section)
    object_list     = model.objects.filter(start_casting="").order_by('serial_num')
    d = {'pailnumform_cas':pailnumform_cas,'pailcorrectform':pailcorrectform, 'object_list':object_list}
    return render(request,'casting.html',d)


# #ログイン後右側の画面（進捗管理）Suemasu-41348 修正用
def management(request):
    return render(request,'management.html')

#formについて知るための練習
def kakikomi(request):
    if request.method == 'POST':
        f = KakikomiForm(request.POST)
    else:
        f = KakikomiForm()
    return render(request,'kakikomiform.html',{'form1':f})
