# Generated by Django 2.2.1 on 2019-12-05 05:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileNameModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=50)),
                ('upload_time', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipment_results', models.CharField(max_length=50, verbose_name='出荷実績')),
            ],
        ),
        migrations.CreateModel(
            name='sample2',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pailnum', models.CharField(max_length=50, verbose_name='杭番号')),
                ('emp', models.CharField(max_length=50, verbose_name='空')),
            ],
        ),
        migrations.CreateModel(
            name='sample3',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shipment_results', models.CharField(max_length=10, verbose_name='出荷実績')),
                ('delivery_record', models.CharField(max_length=20, verbose_name='納品実績')),
                ('deliverer', models.CharField(max_length=10, verbose_name='納品者')),
                ('material_inspection', models.CharField(max_length=20, verbose_name='材料検査')),
                ('inspector', models.CharField(max_length=10, verbose_name='検査者')),
                ('pail_num', models.IntegerField(verbose_name='杭番号')),
                ('cross_section', models.CharField(max_length=5, verbose_name='断面')),
                ('casting', models.IntegerField(verbose_name='打設開始')),
                ('start_casting', models.CharField(max_length=20, verbose_name='打設開始時刻')),
                ('caster', models.CharField(max_length=10, verbose_name='打設者')),
                ('correction', models.CharField(max_length=20, verbose_name='修正時刻')),
                ('corrector', models.CharField(max_length=10, verbose_name='修正者')),
            ],
        ),
    ]
