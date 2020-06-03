# Generated by Django 2.0.4 on 2018-05-11 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nopasswordwaitingforemailconfirm',
            name='cookie',
            field=models.CharField(default='9f75e9ad61e24a7b9270', editable=False, max_length=25, unique=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.CharField(default='ca86c56', editable=False, max_length=32, primary_key=True, serialize=False, unique=True),
        ),
        migrations.AlterField(
            model_name='usercookie',
            name='cookie',
            field=models.CharField(editable=False, max_length=25),
        ),
    ]
