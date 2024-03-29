# Generated by Django 4.1.7 on 2023-03-04 20:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Weather',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('codeInsee', models.IntegerField(null=True, unique=True)),
                ('date', models.DateField(default=django.utils.timezone.now)),
                ('tmin', models.IntegerField(null=True)),
                ('tmax', models.IntegerField(null=True)),
                ('probarain', models.IntegerField(null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='region',
            name='regionVisited',
        ),
    ]
