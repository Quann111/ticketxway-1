# Generated by Django 5.0.3 on 2024-04-04 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('print', '0004_alter_ticketmodel_ticket_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketmodel',
            name='ticket_date',
            field=models.DateField(max_length=10),
        ),
    ]
