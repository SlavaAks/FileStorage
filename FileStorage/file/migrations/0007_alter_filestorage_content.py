# Generated by Django 3.2.13 on 2022-04-19 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('file', '0006_alter_filestorage_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filestorage',
            name='content',
            field=models.FileField(max_length=30, upload_to='file/<django.db.models.query_utils.DeferredAttribute object at 0x7fe106e06860>/%Y/%m/%d/%H%M%S'),
        ),
    ]