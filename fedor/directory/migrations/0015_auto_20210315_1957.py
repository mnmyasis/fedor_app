# Generated by Django 3.1 on 2021-03-15 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('directory', '0014_auto_20210315_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='synceas',
            name='type_packing_fv',
            field=models.TextField(blank=True, null=True),
        ),
    ]