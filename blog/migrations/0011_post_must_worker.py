# Generated by Django 2.2 on 2020-08-18 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_auto_20200602_0540'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='must_worker',
            field=models.ManyToManyField(related_name='must', to='blog.SyainTable'),
        ),
    ]
