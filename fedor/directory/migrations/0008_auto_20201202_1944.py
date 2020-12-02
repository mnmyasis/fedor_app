# Generated by Django 3.1 on 2020-12-02 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0007_auto_20201201_1817'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupChangeTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('change', models.TextField(blank=True)),
                ('search', models.TextField()),
            ],
            options={
                'db_table': 'group_change_table',
            },
        ),
        migrations.DeleteModel(
            name='EAS',
        ),
    ]