# Generated by Django 3.1 on 2020-08-28 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crawlzero', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
