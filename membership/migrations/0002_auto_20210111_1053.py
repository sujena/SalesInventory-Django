# Generated by Django 3.1.2 on 2021-01-11 05:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('membership', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customer',
            old_name='f_name',
            new_name='first_name',
        ),
        migrations.RenameField(
            model_name='customer',
            old_name='l_name',
            new_name='last_name',
        ),
    ]
