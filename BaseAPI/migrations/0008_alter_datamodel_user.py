# Generated by Django 4.2.2 on 2023-07-14 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseAPI', '0007_rename_uid_datamodel_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datamodel',
            name='user',
            field=models.CharField(max_length=20, null=True),
        ),
    ]