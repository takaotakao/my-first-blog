# Generated by Django 2.2 on 2020-06-02 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20200515_0622'),
    ]

    operations = [
        migrations.AddField(
            model_name='kojintourokutable',
            name='KojinTourokuNo',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='kojintourokutable',
            name='SyainNo',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
