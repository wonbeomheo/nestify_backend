# Generated by Django 5.1.3 on 2024-12-04 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='nestifyuser',
            name='name',
            field=models.CharField(default='user-289', max_length=255),
        ),
    ]
