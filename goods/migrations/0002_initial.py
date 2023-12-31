# Generated by Django 4.2.3 on 2023-09-12 11:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('goods', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodscollect',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户'),
        ),
        migrations.AddField(
            model_name='goods',
            name='cate',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='goods.category', verbose_name='商品类别'),
        ),
    ]
