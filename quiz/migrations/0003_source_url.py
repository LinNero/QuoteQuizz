# Generated by Django 3.2.6 on 2021-08-07 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0002_category_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='source',
            name='url',
            field=models.CharField(default='', max_length=255),
            preserve_default=False,
        ),
    ]
