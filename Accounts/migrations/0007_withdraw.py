# Generated by Django 5.1.6 on 2025-02-19 06:53

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Accounts", "0006_alter_address_state_bankdetails"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="withdraw",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("wallet_address", models.CharField(max_length=255)),
                ("amount", models.DecimalField(decimal_places=8, max_digits=20)),
                ("verification_code", models.CharField(max_length=6)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "user_profile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="withdraw_details",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
