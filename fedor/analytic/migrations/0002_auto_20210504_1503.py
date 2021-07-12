# Generated by Django 3.1 on 2021-05-04 15:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0001_initial'),
        ('analytic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='matchingstatistic',
            name='number_competitor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directory.competitors'),
        ),
    ]