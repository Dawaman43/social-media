# Generated by Django 5.1.5 on 2025-01-28 14:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_rename_created_at_comment_comment_date_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='share',
            old_name='created_at',
            new_name='share_date',
        ),
        migrations.AlterField(
            model_name='share',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shares', to='home.userpost'),
        ),
    ]
