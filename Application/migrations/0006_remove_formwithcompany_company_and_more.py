# Generated by Django 4.2.3 on 2023-10-03 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0005_drawedimplantorcrown_specificparameter_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formwithcompany',
            name='company',
        ),
        migrations.RemoveField(
            model_name='formwithcompany',
            name='question',
        ),
        migrations.DeleteModel(
            name='FormAnswers',
        ),
        migrations.DeleteModel(
            name='FormQuestion',
        ),
        migrations.DeleteModel(
            name='FormWithCompany',
        ),
    ]