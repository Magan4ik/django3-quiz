# Generated by Django 4.1.1 on 2023-10-13 08:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_alter_quiz_answers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='quiz',
            old_name='variants',
            new_name='tags',
        ),
    ]
