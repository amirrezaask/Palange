# Generated by Django 3.0.4 on 2020-06-12 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0003_auto_20200612_1937'),
    ]

    operations = [
        migrations.AlterField(
            model_name='organizerprofile',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
