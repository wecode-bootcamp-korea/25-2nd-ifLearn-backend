# Generated by Django 3.2.7 on 2021-10-21 11:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='deleted_at',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]
