# Generated by Django 2.2 on 2019-10-14 06:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_auto_20191014_0610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='compleat_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='fixed_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
