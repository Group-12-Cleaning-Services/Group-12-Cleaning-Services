# Generated by Django 4.2.9 on 2024-07-20 13:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_medicine_thumnail'),
    ]

    operations = [
        migrations.RenameField(
            model_name='medicine',
            old_name='thumnail',
            new_name='thumbnail',
        ),
    ]
