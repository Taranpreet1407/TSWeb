# Generated by Django 2.2.17 on 2020-11-17 11:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_fulluserdata_payment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payments',
            fields=[
                ('intern_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='home.InternData')),
                ('payment_id', models.CharField(max_length=254)),
                ('order_id', models.CharField(max_length=254)),
                ('signature', models.CharField(max_length=254)),
            ],
        ),
    ]
