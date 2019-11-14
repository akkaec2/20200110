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
# from django.contrib import admin
# from django.urls import path,include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('accounts.urls')),
# ]

from django.conf.urls import url 
from django.contrib import admin 
from accounts import views 
from django.contrib.auth import login,logout
 
urlpatterns = [ 
    url(r'^admin/', admin.site.urls), 
    url(r'^create/$', views.create_account, name='create_account'), 
    url(r'^$', views.account_login, name='login'), #r'^login/$'から変更
    # url(r'^operate$', views.main_operate, name='main_operate'),
    url(r'^$', views.account_login, name='logout'), #login画面に戻る
    url(r'^collation/$', views.collation, name='collation'), #杭照合画面表示
    url(r'^casting/$', views.casting, name='casting'), #杭打設確認画面表示
    url(r'^confirm/$', views.confirm, name='confirm'), #受入検査確認画面表示
]
