# Generated by Django 4.2.2 on 2023-07-13 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseAPI', '0005_rename_slope_datamodel_slop'),
    ]

    operations = [
        migrations.AddField(
            model_name='datamodel',
            name='uid',
            field=models.TextField(null=True),
        ),
    ]
