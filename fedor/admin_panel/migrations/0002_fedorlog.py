# Generated by Django 3.1 on 2021-05-17 14:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('admin_panel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FedorLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(blank=True)),
                ('sku_id', models.BigIntegerField(default=0)),
                ('eas_id', models.BigIntegerField(default=0)),
                ('action', models.IntegerField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'fedor_log',
                'ordering': ['-create_date'],
            },
        ),
    ]
