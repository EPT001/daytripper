# Generated by Django 4.2.6 on 2024-03-17 18:33

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("myapp", "0002_review_bookmark"),
    ]

    operations = [
        migrations.AddField(
            model_name="bookmark",
            name="place_name",
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]