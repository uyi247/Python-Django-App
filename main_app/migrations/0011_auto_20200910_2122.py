# Generated by Django 3.1 on 2020-09-10 21:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0010_auto_20200910_1317'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collectionrating',
            name='rating',
            field=models.IntegerField(default=5),
        ),
    ]
