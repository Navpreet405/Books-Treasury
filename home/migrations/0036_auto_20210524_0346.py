# Generated by Django 3.2.3 on 2021-05-23 22:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0035_alter_order_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='price',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='seller',
            name='price',
            field=models.FloatField(),
        ),
    ]