# Generated by Django 5.1.3 on 2024-12-04 13:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_nestifyuser_membership_alter_membership_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nestifyuser',
            name='name',
            field=models.CharField(default='user-184', max_length=255),
        ),
    ]