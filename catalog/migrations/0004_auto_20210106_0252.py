# Generated by Django 3.1.5 on 2021-01-06 02:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20210106_0029'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['title', 'author']},
        ),
    ]
