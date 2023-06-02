# Generated by Django 4.2.1 on 2023-06-02 06:17

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('search_phrase', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('frequency', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=255)),
                ('email_id', models.EmailField(max_length=254)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('frequency', models.CharField(max_length=20)),
            ],
        ),
    ]
