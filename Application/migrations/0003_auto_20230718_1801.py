# Generated by Django 3.2.16 on 2023-07-18 15:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Application', '0002_illnesslabel_illness_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dicomreport',
            name='image_report',
        ),
        migrations.RemoveField(
            model_name='dicomreport',
            name='report_type',
        ),
        migrations.DeleteModel(
            name='DicomUploadProgress',
        ),
        migrations.DeleteModel(
            name='DicomAnalysisType',
        ),
        migrations.DeleteModel(
            name='DicomReport',
        ),
    ]
