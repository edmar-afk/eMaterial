# Generated by Django 5.0.4 on 2024-05-03 12:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_materials_borrowed_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materials',
            name='borrowed_date',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 5, 3, 12, 56, 26, 174044, tzinfo=datetime.timezone.utc), null=True),
        ),
        migrations.AlterField(
            model_name='materials',
            name='deadline',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2024, 5, 3, 12, 56, 26, 174044, tzinfo=datetime.timezone.utc), null=True),
        ),
    ]
