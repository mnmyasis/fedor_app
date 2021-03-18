# Generated by Django 3.1 on 2021-03-15 18:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0008_auto_20201202_1944'),
    ]

    operations = [
        migrations.CreateModel(
            name='BarcodeEAS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('barcode_id', models.BigIntegerField()),
                ('value', models.TextField(blank=True)),
            ],
            options={
                'db_table': 'barcode_eas',
            },
        ),
        migrations.CreateModel(
            name='SyncEAS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eas_id', models.BigIntegerField()),
                ('status', models.IntegerField(default=1)),
                ('umbrella_brand', models.TextField(blank=True)),
                ('tn_fv', models.TextField(blank=True)),
                ('registration_tm', models.TextField(blank=True)),
                ('corporation', models.TextField(blank=True)),
                ('manufacturer', models.TextField(blank=True)),
                ('rx_otc', models.TextField(blank=True)),
                ('trade_name_rus', models.TextField(blank=True)),
                ('trade_name_eng', models.TextField(blank=True)),
                ('pack_key', models.TextField(blank=True)),
                ('type_packing_fv', models.TextField(blank=True)),
                ('dosage', models.TextField(blank=True)),
                ('volwe', models.TextField(blank=True)),
                ('numero', models.TextField(blank=True)),
                ('tastes_and_parentheses_fv', models.TextField(blank=True)),
                ('vendor_code', models.TextField(blank=True)),
                ('divisible_packaging', models.TextField(blank=True)),
                ('size', models.TextField(blank=True)),
                ('age', models.TextField(blank=True)),
                ('full_corp', models.TextField(blank=True)),
                ('corp_rus', models.TextField(blank=True)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('update_date', models.DateField(auto_now=True)),
                ('barcode', models.ManyToManyField(to='directory.BarcodeEAS')),
            ],
            options={
                'db_table': 'sync_eas',
            },
        ),
        migrations.CreateModel(
            name='EAS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eas_id', models.BigIntegerField()),
                ('status', models.IntegerField(default=1)),
                ('umbrella_brand', models.TextField(blank=True)),
                ('tn_fv', models.TextField(blank=True)),
                ('registration_tm', models.TextField(blank=True)),
                ('corporation', models.TextField(blank=True)),
                ('manufacturer', models.TextField(blank=True)),
                ('rx_otc', models.TextField(blank=True)),
                ('trade_name_rus', models.TextField(blank=True)),
                ('trade_name_eng', models.TextField(blank=True)),
                ('pack_key', models.TextField(blank=True)),
                ('type_packing_fv', models.TextField(blank=True)),
                ('dosage', models.TextField(blank=True)),
                ('volwe', models.TextField(blank=True)),
                ('numero', models.TextField(blank=True)),
                ('tastes_and_parentheses_fv', models.TextField(blank=True)),
                ('vendor_code', models.TextField(blank=True)),
                ('divisible_packaging', models.TextField(blank=True)),
                ('size', models.TextField(blank=True)),
                ('age', models.TextField(blank=True)),
                ('full_corp', models.TextField(blank=True)),
                ('corp_rus', models.TextField(blank=True)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('update_date', models.DateField(auto_now=True)),
                ('barcode', models.ManyToManyField(to='directory.BarcodeEAS')),
            ],
            options={
                'db_table': 'eas',
            },
        ),
    ]
