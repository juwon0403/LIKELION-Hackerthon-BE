# Generated by Django 4.2.3 on 2023-07-22 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppLevel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level_value', models.IntegerField(default=0)),
                ('level_comment', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='AppInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('image', models.ImageField(upload_to='images/')),
                ('summary', models.CharField(max_length=200)),
                ('detail', models.TextField()),
                ('link', models.TextField()),
                ('is_downloaded', models.BooleanField()),
                ('field', models.CharField(max_length=20)),
                ('level', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='levels', to='applist.applevel')),
            ],
        ),
    ]
