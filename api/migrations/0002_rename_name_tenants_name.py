# Generated by Django 3.2.5 on 2021-07-21 17:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tenants',
            old_name='Name',
            new_name='name',
        ),
    ]
