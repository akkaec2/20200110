from django.db import models
# from django import forms

#https://eiry.bitbucket.io/tutorials/tutorial/crud_read.html
# Create your models here.
class PailnumModel(models.Model):
    pail_num        = models.CharField(max_length=10)
    pail_detail_num = models.CharField(max_length=10)

    def __str__(self):
        return self.pail_num,self.pail_detail_num