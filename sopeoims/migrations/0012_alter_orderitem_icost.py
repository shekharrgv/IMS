# Generated by Django 4.2.3 on 2023-08-07 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sopeoims', '0011_notreceived'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='ICost',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]
