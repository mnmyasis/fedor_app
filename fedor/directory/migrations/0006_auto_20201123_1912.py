# Generated by Django 3.1 on 2020-11-23 16:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0005_auto_20201123_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientdirectory',
            name='number_competitor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directory.numbercompetitor'),
        ),
    ]