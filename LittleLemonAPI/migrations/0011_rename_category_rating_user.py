# Generated by Django 4.1.7 on 2023-03-27 08:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("LittleLemonAPI", "0010_rating"),
    ]

    operations = [
        migrations.RenameField(
            model_name="rating", old_name="category", new_name="user",
        ),
    ]