# Generated by Django 3.2.16 on 2023-07-18 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Application3d', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dicomanalysistype',
            name='slug',
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]
