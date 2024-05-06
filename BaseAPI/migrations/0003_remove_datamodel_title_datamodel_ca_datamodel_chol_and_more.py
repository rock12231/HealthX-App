# Generated by Django 4.2.2 on 2023-06-28 10:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BaseAPI', '0002_rename_designmodel_datamodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='datamodel',
            name='title',
        ),
        migrations.AddField(
            model_name='datamodel',
            name='ca',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='datamodel',
            name='chol',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='datamodel',
            name='cp',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='datamodel',
            name='exang',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='datamodel',
            name='fbs',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='datamodel',
            name='oldpeak',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='datamodel',
            name='restecg',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='datamodel',
            name='slope',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='datamodel',
            name='thal',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='datamodel',
            name='thalach',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='datamodel',
            name='trestbps',
            field=models.IntegerField(null=True),
        ),
    ]
