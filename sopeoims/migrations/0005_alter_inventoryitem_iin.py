# Generated by Django 4.2.3 on 2023-08-07 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sopeoims', '0004_alter_inventoryitem_icost_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventoryitem',
            name='IIN',
            field=models.CharField(blank=True, max_length=10, unique=True),
        ),
    ]