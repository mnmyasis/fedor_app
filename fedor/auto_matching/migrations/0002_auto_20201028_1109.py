# Generated by Django 3.1 on 2020-10-28 08:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auto_matching', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='BaseDirectory',
        ),
        migrations.DeleteModel(
            name='ClientDirectory',
        ),
    ]