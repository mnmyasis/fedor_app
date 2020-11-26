# Generated by Django 3.1 on 2020-11-23 16:06

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('manual_matching', '0007_auto_20201110_1852'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='finalmatching',
            options={},
        ),
        migrations.RenameField(
            model_name='finalmatching',
            old_name='date',
            new_name='update_date',
        ),
        migrations.RenameField(
            model_name='manualmatchingdata',
            old_name='date_update',
            new_name='create_date',
        ),
        migrations.RenameField(
            model_name='manualmatchingdata',
            old_name='date',
            new_name='update_date',
        ),
        migrations.AddField(
            model_name='finalmatching',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]