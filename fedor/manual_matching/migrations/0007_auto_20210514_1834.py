# Generated by Django 3.1 on 2021-05-14 18:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0001_initial'),
        ('manual_matching', '0006_auto_20210505_2342'),
    ]

    operations = [
        migrations.AlterField(
            model_name='finalmatching',
            name='number_competitor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directory.competitors'),
        ),
        migrations.AlterField(
            model_name='manualmatchingdata',
            name='number_competitor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directory.competitors'),
        ),
    ]
