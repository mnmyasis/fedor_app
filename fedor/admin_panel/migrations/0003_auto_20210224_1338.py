# Generated by Django 3.1 on 2021-02-24 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0002_auto_20210224_1331'),
    ]

    operations = [
        migrations.CreateModel(
            name='AccessLevel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.IntegerField()),
                ('level_name', models.CharField(max_length=150)),
            ],
        ),
        migrations.RemoveField(
            model_name='profile',
            name='level',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='name',
        ),
        migrations.AddField(
            model_name='profile',
            name='access_level',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='admin_panel.accesslevel'),
            preserve_default=False,
        ),
    ]