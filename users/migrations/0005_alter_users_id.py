# Generated by Django 5.2 on 2025-05-04 08:37

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_users_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='id',
            field=models.UUIDField(default=uuid.UUID('f8f44a2b-e5a7-439a-af59-0859ba0296d1'), primary_key=True, serialize=False),
        ),
    ]
