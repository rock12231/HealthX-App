# Generated by Django 4.2.2 on 2023-06-26 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilemodel',
            name='status',
            field=models.CharField(choices=[('process', 'In Process'), ('pending', 'Pending'), ('done', 'Done'), ('onhold', 'On Hold')], max_length=10),
        ),
    ]
