# Generated by Django 4.2.3 on 2023-07-30 05:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('applist', '0002_categorytag_alter_appinfo_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhoneModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='appinfo',
            name='model',
            field=models.ManyToManyField(related_name='phonemodel', to='applist.phonemodel'),
        ),
    ]
