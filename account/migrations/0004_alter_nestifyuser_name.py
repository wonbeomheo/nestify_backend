# Generated by Django 5.1.3 on 2024-12-04 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_membership_nestifyuser_balance_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nestifyuser',
            name='name',
            field=models.CharField(default='user-363', max_length=255),
        ),
    ]
