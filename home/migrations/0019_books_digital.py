# Generated by Django 3.2.3 on 2021-05-21 23:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_order_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='books',
            name='digital',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]