# Generated by Django 4.2.3 on 2023-08-13 19:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sopeoims', '0022_receivedtransaction_canceledtransaction'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='receivedtransaction',
            name='transaction',
        ),
        migrations.DeleteModel(
            name='CanceledTransaction',
        ),
        migrations.DeleteModel(
            name='ReceivedTransaction',
        ),
    ]