# Generated by Django 3.1.6 on 2021-03-30 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0002_offers_mail_body'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sales',
            name='offer',
        ),
        migrations.AddField(
            model_name='sales',
            name='discount',
            field=models.IntegerField(default=0),
        ),
    ]
