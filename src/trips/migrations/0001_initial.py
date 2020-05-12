# Generated by Django 3.0.4 on 2020-03-25 07:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user_auth', '0001_add_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128, verbose_name='Title')),
                ('description', models.TextField(max_length=1024, verbose_name='Description')),
                ('start_date', models.DateTimeField(verbose_name='Start Date')),
                ('end_date', models.DateTimeField(verbose_name='End Date')),
                ('capacity', models.PositiveIntegerField(verbose_name='Capacity')),
                ('organizer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user_auth.Profile', verbose_name='Organizer')),
            ],
            options={
                'verbose_name': 'Trip',
                'verbose_name_plural': 'Trips',
            },
        ),
    ]
