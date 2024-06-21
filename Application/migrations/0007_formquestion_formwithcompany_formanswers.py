# Generated by Django 4.2.3 on 2023-10-03 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0004_buyedextrapackage_buyedpackage_extrapackage_package_and_more'),
        ('Application', '0006_remove_formwithcompany_company_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FormQuestion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(blank=True, max_length=255, null=True)),
                ('question_tr', models.CharField(blank=True, max_length=255, null=True)),
                ('answers', models.CharField(blank=True, max_length=1000, null=True)),
                ('answers_tr', models.CharField(blank=True, max_length=1000, null=True)),
                ('slug', models.CharField(blank=True, max_length=32, null=True)),
                ('queue', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FormWithCompany',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('required', models.BooleanField()),
                ('is_active', models.BooleanField()),
                ('form_slug', models.CharField(blank=True, max_length=32, null=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.company')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Application.formquestion')),
            ],
        ),
        migrations.CreateModel(
            name='FormAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_slug', models.CharField(max_length=32)),
                ('group_slug', models.CharField(max_length=100)),
                ('date', models.DateTimeField(blank=True, null=True)),
                ('answer', models.CharField(blank=True, max_length=255, null=True)),
                ('specify', models.CharField(blank=True, max_length=255, null=True)),
                ('form', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Application.formwithcompany')),
            ],
        ),
    ]