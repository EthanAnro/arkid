# Generated by Django 3.1.7 on 2021-04-05 11:19

from django.db import migrations


def add_default_tenant(apps, schema_editor):
    from tenant.models import Tenant

    Tenant.objects.create(
        name="Default Tenant",
        slug="default",
    )
    

class Migration(migrations.Migration):

    dependencies = [
        ('siteadmin', '0001_add_default_super_user'),
    ]

    operations = [
        migrations.RunPython(add_default_tenant),
    ]