# Generated by Django 3.1 on 2020-12-12 11:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('directory', '0008_auto_20201202_1944'),
    ]

    operations = [
        migrations.CreateModel(
            name='MatchingStatistic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('action', models.IntegerField()),
                ('sku_id', models.IntegerField()),
                ('eas_id', models.IntegerField()),
                ('create_date', models.DateTimeField(auto_now=True)),
                ('number_competitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directory.numbercompetitor')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'matching_statistic',
            },
        ),
    ]