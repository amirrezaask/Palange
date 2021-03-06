# Generated by Django 3.0.4 on 2020-04-24 15:59

from django.db import migrations, models
import django.db.models.deletion
import trips.models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0001_add_profile'),
        ('trips', '0003_auto_20200423_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='image',
            field=models.ImageField(upload_to=trips.models.image_upload_name, verbose_name='Image'),
        ),
        migrations.CreateModel(
            name='PreRegister',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_approved', models.BooleanField(default=False, verbose_name='Is Approved')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user_auth.Profile', verbose_name='Profile')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='trips.Trip', verbose_name='Trip')),
            ],
            options={
                'verbose_name': 'PreRegister',
                'verbose_name_plural': 'PreRegisters',
                'unique_together': {('trip', 'profile')},
            },
        ),
    ]
