# Generated by Django 3.1.5 on 2021-01-05 21:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='author',
            old_name='data_of_birth',
            new_name='date_of_birth',
        ),
    ]
