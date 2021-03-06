# Generated by Django 3.1 on 2021-05-20 18:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
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
            name='EAS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eas_id', models.BigIntegerField()),
                ('status', models.IntegerField(default=1)),
                ('barcode', models.TextField(blank=True, null=True)),
                ('umbrella_brand', models.TextField(blank=True)),
                ('tn_fv', models.TextField(blank=True)),
                ('registration_tm', models.TextField(blank=True)),
                ('corporation', models.TextField(blank=True)),
                ('manufacturer', models.TextField(blank=True)),
                ('rx_otc', models.TextField(blank=True)),
                ('trade_name_rus', models.TextField(blank=True)),
                ('trade_name_eng', models.TextField(blank=True)),
                ('pack_key', models.TextField(blank=True)),
                ('fv_short', models.TextField(blank=True)),
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
            ],
            options={
                'db_table': 'eas',
            },
        ),
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
        migrations.CreateModel(
            name='SyncEAS',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eas_id', models.BigIntegerField()),
                ('status', models.IntegerField(default=1)),
                ('barcode', models.TextField(blank=True, null=True)),
                ('umbrella_brand', models.TextField(blank=True, null=True)),
                ('tn_fv', models.TextField(blank=True, null=True)),
                ('registration_tm', models.TextField(blank=True, null=True)),
                ('corporation', models.TextField(blank=True, null=True)),
                ('manufacturer', models.TextField(blank=True, null=True)),
                ('rx_otc', models.TextField(blank=True, null=True)),
                ('trade_name_rus', models.TextField(blank=True, null=True)),
                ('trade_name_eng', models.TextField(blank=True, null=True)),
                ('pack_key', models.TextField(blank=True, null=True)),
                ('fv_short', models.TextField(blank=True, null=True)),
                ('type_packing_fv', models.TextField(blank=True, null=True)),
                ('dosage', models.TextField(blank=True, null=True)),
                ('volwe', models.TextField(blank=True, null=True)),
                ('numero', models.TextField(blank=True, null=True)),
                ('tastes_and_parentheses_fv', models.TextField(blank=True, null=True)),
                ('vendor_code', models.TextField(blank=True, null=True)),
                ('divisible_packaging', models.TextField(blank=True, null=True)),
                ('size', models.TextField(blank=True, null=True)),
                ('age', models.TextField(blank=True, null=True)),
                ('full_corp', models.TextField(blank=True, null=True)),
                ('corp_rus', models.TextField(blank=True, null=True)),
                ('create_date', models.DateField(auto_now_add=True)),
                ('update_date', models.DateField(auto_now=True)),
            ],
            options={
                'db_table': 'sync_eas',
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
    ]
