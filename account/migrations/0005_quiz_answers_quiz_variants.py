# Generated by Django 4.1.1 on 2023-09-26 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='answers',
            field=models.JSONField(default=[]),
        ),
        migrations.AddField(
            model_name='quiz',
            name='variants',
            field=models.JSONField(default=[]),
        ),
    ]
