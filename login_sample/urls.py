"""login_sample URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url 
from django.contrib import admin 
from accounts import views 
from django.contrib.auth import login,logout
from django.urls import path
import logging

# app_name = 'accounts'

urlpatterns = [ 
    url(r'^admin/', admin.site.urls), 
    url(r'^create/$', views.create_account, name='create_account'), 
    url(r'^$', views.account_login, name='login'),                    #login画面　
    url(r'^$', views.account_login, name='logout'),                   #login画面に戻る 
    url(r'^fileread/$', views.PostImport.as_view(), name='fileread'), #納品確認　csv受入
    url(r'^collation/$', views.collation, name='collation'),          #納品確認
    url(r'^confirm/$', views.confirm, name='confirm'),                #材料検査
    url(r'^casting/$', views.casting, name='casting'),                #打設
    url(r'^casting1/$', views.pailcorrectview, name='correct'),        #打設　修正用
    url(r'^management/$', views.management, name='management'),   #進捗管理
    # url(r'^management/$', views.managementview, name='management'),   #進捗管理



#練習
    url(r'^keijiban/$', views.kakikomi, name='kakikomi'),
    
]
