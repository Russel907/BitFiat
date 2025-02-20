# Generated by Django 5.1.6 on 2025-02-19 09:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Accounts", "0008_alter_withdraw_user_profile_deposit"),
    ]

    operations = [
        migrations.AddField(
            model_name="userprofile",
            name="referral_code",
            field=models.CharField(blank=True, max_length=10, null=True, unique=True),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="referred_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="referred_users",
                to="Accounts.userprofile",
            ),
        ),
        migrations.AddField(
            model_name="userprofile",
            name="referred_count",
            field=models.IntegerField(default=0),
        ),
    ]
