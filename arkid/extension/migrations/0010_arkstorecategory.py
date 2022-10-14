# Generated by Django 3.2.13 on 2022-09-14 03:15

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('extension', '0009_extension_category_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='ArkStoreCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('is_del', models.BooleanField(default=False, verbose_name='是否删除')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否可用')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='更新时间')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间')),
                ('arkstore_id', models.IntegerField(default=None, null=True, verbose_name='ArkStoreID')),
                ('arkstore_name', models.CharField(blank=True, default='', max_length=128, null=True, verbose_name='ArkStore名称')),
                ('arkstore_parent_id', models.IntegerField(default=None, null=True, verbose_name='ArkStoreParentID')),
                ('arkstore_type', models.CharField(choices=[('app', '应用'), ('extension', '插件')], default='app', max_length=128, verbose_name='类别')),
            ],
            options={
                'verbose_name': 'ArkStore分类',
                'verbose_name_plural': 'ArkStore分类',
            },
        ),
    ]