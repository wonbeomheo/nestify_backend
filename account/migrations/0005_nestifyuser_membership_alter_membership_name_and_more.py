# Generated by Django 5.1.3 on 2024-12-04 13:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_nestifyuser_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='nestifyuser',
            name='membership',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='account.membership'),
        ),
        migrations.AlterField(
            model_name='membership',
            name='name',
            field=models.CharField(choices=[('free', 'Free'), ('nestian', 'Nestian')], default='free', max_length=10),
        ),
        migrations.AlterField(
            model_name='nestifyuser',
            name='name',
            field=models.CharField(default='user-410', max_length=255),
        ),
    ]
