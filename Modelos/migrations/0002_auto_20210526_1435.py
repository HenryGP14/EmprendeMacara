# Generated by Django 3.0.8 on 2021-05-26 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Modelos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='eliminado',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='servicios',
            name='eliminado',
            field=models.BooleanField(default=False),
        ),
    ]