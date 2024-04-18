# Generated by Django 4.2.7 on 2024-04-18 14:33

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('modules', '0004_module_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='module',
            name='liked_users',
            field=models.ManyToManyField(related_name='liked_modules', to=settings.AUTH_USER_MODEL, verbose_name='лайкнувшие'),
        ),
    ]
