# Generated by Django 4.2.7 on 2024-01-05 19:24

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("chats", "0002_conversation_last_message"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="message",
            options={"ordering": ("-created_at",)},
        ),
    ]