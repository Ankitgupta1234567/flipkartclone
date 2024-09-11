# Generated by Django 5.1 on 2024-08-21 09:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Products',
            fields=[
                ('productid', models.IntegerField(primary_key=True, serialize=False)),
                ('productname', models.CharField(max_length=100)),
                ('category', models.CharField(choices=[('moblie', 'moblie'), ('moblie', 'moblie'), ('moblie', 'moblie'), ('moblie', 'moblie')], max_length=100)),
                ('description', models.TextField()),
                ('price', models.FloatField()),
                ('images', models.ImageField(upload_to='photos')),
                ('userid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('orderid', models.IntegerField(primary_key=True, serialize=False)),
                ('qty', models.PositiveIntegerField(default=0)),
                ('userid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('productid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.products')),
            ],
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('qty', models.PositiveIntegerField(default=0)),
                ('userid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('productid', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.products')),
            ],
        ),
    ]
