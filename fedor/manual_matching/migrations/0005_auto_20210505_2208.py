# Generated by Django 3.1 on 2021-05-05 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manual_matching', '0004_auto_20210505_2206'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manualmatchingdata',
            name='number_competitor',
            field=models.IntegerField(default=1),
        ),
    ]