# Generated by Django 2.0.7 on 2018-09-24 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='kryptosuser',
            name='answer_log',
            field=models.TextField(default={}),
        ),
    ]
