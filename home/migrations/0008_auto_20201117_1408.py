# Generated by Django 2.2.17 on 2020-11-17 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20201117_1339'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='workdata',
            name='no_enrolled',
        ),
        migrations.AlterField(
            model_name='workdata',
            name='intern_id',
            field=models.IntegerField(null=True),
        ),
    ]
