from django.db import models
from datetime import datetime
from django.utils import timezone
import logging

# from django import forms
#https://eiry.bitbucket.io/tutorials/tutorial/crud_read.html

# #table 2019/12/4
# class sample3(models.Model):
#     shipment_results = models.CharField('出荷実績',max_length=10)
#     delivery_record = models.CharField('納品実績',max_length=20)
#     deliverer = models.CharField('納品者',max_length=10)
#     material_inspection = models.CharField('材料検査',max_length=20)
#     inspector = models.CharField('検査者',max_length=10)
#     pail_num = models.IntegerField('杭番号')
#     cross_section = models.CharField('断面',max_length=5)
#     casting = models.IntegerField('打設開始')
#     start_casting = models.CharField('打設開始時刻',max_length=20)
#     caster = models.CharField('打設者',max_length=10)
#     correction = models.CharField('修正時刻',max_length=20)
#     corrector = models.CharField('修正者',max_length=10)

#     def __str__(self):
#         return self.shipment_results,self.delivery_record,self.deliverer,\
#             self.material_inspection,self.inspector,self.pail_num,self.cross_section,\
#             self.casting,self.start_casting,self.caster,self.correction,self.corrector

# class Post1(models.Model):
#     shipment_results    = models.CharField('出荷実績',max_length=20,primary_key=True)
#     delivery_record     = models.CharField('納品実績',max_length=40,null=True)
#     deliverer           = models.CharField('納品確認者',max_length=10,null=True)
#     material_inspection = models.CharField('材料検査',max_length=40,null=True)
#     inspector           = models.CharField('検査者',max_length=10,null=True)
#     pail_num = models.IntegerField('杭番号')
#     pail_num            = models.CharField('杭番号',max_length=5,null=True)
#     cross_section       = models.CharField('断面',max_length=5,null=True)
#     casting = models.IntegerField('打設開始')
#     casting             = models.CharField('打設開始',max_length=5,null=True)
#     start_casting       = models.CharField('打設開始時刻',max_length=40,null=True)
#     caster              = models.CharField('打設者',max_length=10,null=True)
#     correction          = models.CharField('修正時刻',max_length=40,null=True)
#     corrector           = models.CharField('修正者',max_length=10,null=True)

#     def __str__(self):
#         return self.shipment_results,self.delivery_record,self.deliverer,\
#             self.material_inspection,self.inspector,self.pail_num,self.cross_section,\
#             self.start_casting,self.caster,self.correction,self.corrector


# #csvupload方法を知るためのもの
# class FileNameModel(models.Model):
#     #file_name : ファイル名
#     file_name = models.CharField(max_length = 50)
#     #upload_time : アップロード日時(デフォルトで現在日時が入る)
#     upload_time = models.DateTimeField(default = datetime.now)

#csvを読み込み複数行（null有）の表を造るためのもの
# class Post2(models.Model):
#     shipment_results = models.CharField('出荷実績', max_length=50,primary_key=True)
#     delivery_record  = models.CharField('納品実績',max_length=50)
#     deliverer        = models.CharField('納品確認者',max_length=10)

#     def __str__(self):
#         return self.shipment_results,self.delivery_record,self.deliverer

#csvを読み込み複数行（null有）の表を造るためのもの
# class Post3(models.Model):
#     shipment_results = models.CharField('出荷実績', max_length=50,primary_key=True)
#     delivery_record  = models.DateTimeField('納品実績',max_length=20, null = True)
#     deliverer        = models.CharField('納品確認者',max_length=10)

#     def __str__(self):
#         return self.shipment_results,self.delivery_record,self.deliverer

class Post4(models.Model):
    serial_num          = models.CharField('出荷実績',max_length=20,primary_key=True)
    delivery_record     = models.CharField('納品実績',max_length=40)
    deliverer           = models.CharField('納品確認者',max_length=10)
    material_inspection = models.CharField('材料検査',max_length=40)
    inspector           = models.CharField('検査者',max_length=10)
    pail_num            = models.CharField('杭番号',max_length=5)
    cross_section       = models.CharField('断面',max_length=5)
    start_casting       = models.CharField('打設時刻',max_length=40)
    caster              = models.CharField('打設者',max_length=10)
    correction          = models.CharField('修正時刻',max_length=40)
    corrector           = models.CharField('修正者',max_length=10)

    def __str__(self):
        return self.serial_num,self.delivery_record,self.deliverer,\
            self.material_inspection,self.inspector,self.pail_num,self.cross_section,\
            self.start_casting,self.caster,self.correction,self.corrector