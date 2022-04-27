# Generated by Django 4.0.4 on 2022-04-22 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extension', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tenantextension',
            options={'verbose_name': '租户插件', 'verbose_name_plural': '租户插件'},
        ),
        migrations.AddField(
            model_name='extension',
            name='profile',
            field=models.JSONField(blank=True, default=dict, verbose_name='Setup Profile'),
        ),
        migrations.AddField(
            model_name='tenantextension',
            name='settings',
            field=models.JSONField(blank=True, default=dict, verbose_name='Tenant Settings'),
        ),
        migrations.AddField(
            model_name='tenantextensionconfig',
            name='name',
            field=models.CharField(default='', max_length=128, verbose_name='名称'),
        ),
        migrations.AlterField(
            model_name='extension',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='是否启动'),
        ),
        migrations.AlterField(
            model_name='extension',
            name='is_allow_use_platform_config',
            field=models.BooleanField(default=False, verbose_name='是否允许租户使用平台配置'),
        ),
        migrations.AlterField(
            model_name='tenantextension',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='是否使用'),
        ),
        migrations.AlterField(
            model_name='tenantextension',
            name='use_platform_config',
            field=models.BooleanField(default=False, verbose_name='是否使用平台配置'),
        ),
        migrations.AlterField(
            model_name='tenantextensionconfig',
            name='config',
            field=models.JSONField(blank=True, default=dict, verbose_name='Runtime Config'),
        ),
    ]
