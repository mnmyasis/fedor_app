# Generated by Django 3.1 on 2020-12-24 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchingstatistic',
            name='create_date',
            field=models.DateField(auto_now=True),
        ),
    ]