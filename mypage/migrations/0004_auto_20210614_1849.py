# Generated by Django 3.2.1 on 2021-06-14 09:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mypage', '0003_auto_20210519_2025'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notificationsforlaboratory',
            name='send_user',
        ),
        migrations.RemoveField(
            model_name='notificationsforuser',
            name='send_user',
        ),
        migrations.RemoveField(
            model_name='notificationsforuser',
            name='user',
        ),
    ]
