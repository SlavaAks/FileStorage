# Generated by Django 3.2.13 on 2022-04-19 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0002_filestorage_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filestorage',
            name='content',
            field=models.FileField(max_length=30, upload_to='file/<django.db.models.query_utils.DeferredAttribute object at 0x7f6534862860>/%Y/%m/%d/%H%M%S'),
        ),
    ]
