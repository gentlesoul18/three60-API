# Generated by Django 4.1 on 2023-01-11 13:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("todo", "0005_merge_20221221_1441"),
    ]

    operations = [
        migrations.RenameField(
            model_name="todo",
            old_name="is_deleted",
            new_name="deleted",
        ),
    ]
