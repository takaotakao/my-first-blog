# Generated by Django 2.2 on 2019-10-12 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_title2'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='compleat_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='post',
            name='fixed_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
