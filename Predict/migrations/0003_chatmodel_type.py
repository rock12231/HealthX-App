# Generated by Django 4.2.2 on 2023-06-27 23:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Predict', '0002_alter_chatmodel_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmodel',
            name='type',
            field=models.IntegerField(choices=[(1, 'Doctor'), (0, 'Patient')], default=0),
            preserve_default=False,
        ),
    ]