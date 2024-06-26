# Generated by Django 4.2.3 on 2024-03-18 09:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('User', '0009_profile_added_by_distributor_profile_is_distributor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchaseRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_slug', models.CharField(max_length=50)),
                ('pack_name', models.CharField(max_length=50)),
                ('company_name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('price', models.CharField(max_length=50)),
                ('transaction_status', models.BooleanField(default=False)),
                ('transaction_date', models.DateTimeField(blank=True, null=True)),
                ('transaction_details', models.TextField(blank=True, null=True)),
                ('payment_status', models.BooleanField(default=False)),
                ('payment_date', models.DateTimeField(blank=True, null=True)),
                ('payment_details', models.TextField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'Purchase Records',
            },
        ),
        migrations.CreateModel(
            name='PackagePricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(blank=True, max_length=32, null=True)),
                ('currency', models.CharField(blank=True, max_length=32, null=True)),
                ('monthly_price', models.CharField(blank=True, max_length=32, null=True)),
                ('yearly_price', models.CharField(blank=True, max_length=32, null=True)),
                ('price_per_token', models.CharField(blank=True, max_length=32, null=True)),
                ('package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.package')),
            ],
            options={
                'verbose_name_plural': '12. PackagePricing',
            },
        ),
        migrations.CreateModel(
            name='ExtraPackagePricing',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(blank=True, max_length=32, null=True)),
                ('currency', models.CharField(blank=True, max_length=32, null=True)),
                ('monthly_price', models.CharField(blank=True, max_length=32, null=True)),
                ('yearly_price', models.CharField(blank=True, max_length=32, null=True)),
                ('price_per_token', models.CharField(blank=True, max_length=32, null=True)),
                ('extra_package', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.extrapackage')),
            ],
            options={
                'verbose_name_plural': '13. ExtraPackagePricing',
            },
        ),
    ]
