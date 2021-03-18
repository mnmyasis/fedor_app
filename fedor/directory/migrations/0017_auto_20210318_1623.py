# Generated by Django 3.1 on 2021-03-18 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0016_auto_20210315_2027'),
    ]

    operations = [
        migrations.CreateModel(
            name='Competitors',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='test')),
                ('pharmacy_id', models.BigIntegerField()),
                ('firm_id', models.BigIntegerField(default=0)),
            ],
            options={
                'db_table': 'competitors',
            },
        ),
        migrations.CreateModel(
            name='SKU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku_id', models.BigIntegerField()),
                ('nnt', models.TextField(blank=True)),
                ('name', models.TextField()),
                ('matching_status', models.BooleanField(default=False)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('number_competitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directory.competitors')),
            ],
            options={
                'db_table': 'sku',
                'ordering': ['sku_id'],
            },
        ),
        migrations.CreateModel(
            name='SyncSKU',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sku_id', models.BigIntegerField()),
                ('nnt', models.TextField(blank=True)),
                ('name', models.TextField()),
                ('matching_status', models.BooleanField(default=False)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('update_date', models.DateTimeField(auto_now=True)),
                ('number_competitor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='directory.competitors')),
            ],
            options={
                'db_table': 'sync_sku',
                'ordering': ['sku_id'],
            },
        ),
        migrations.RemoveField(
            model_name='eas',
            name='barcode',
        ),
        migrations.AddField(
            model_name='eas',
            name='barcode',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='BarcodeEAS',
        ),
    ]
