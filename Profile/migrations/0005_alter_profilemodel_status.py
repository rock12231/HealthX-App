# Generated by Django 4.2.2 on 2023-06-27 22:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Profile', '0004_profilemodel_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profilemodel',
            name='status',
            field=models.CharField(choices=[('process', 'In Process'), ('pending', 'Pending'), ('done', 'Done'), ('onhold', 'On Hold')], default='pending', max_length=10),
        ),
    ]