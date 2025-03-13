# Generated by Django 5.1.7 on 2025-03-13 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('uuid', models.UUIDField(primary_key=True, serialize=False)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('version', models.IntegerField(default=0)),
            ],
            options={
                'constraints': [models.UniqueConstraint(fields=('uuid',), name='unique_wallet_uuid')],
            },
        ),
    ]
