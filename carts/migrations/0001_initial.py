# Generated by Django 4.2.3 on 2023-09-12 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Carts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('selected', models.BooleanField(default=True, verbose_name='勾选状态')),
                ('good_count', models.IntegerField(verbose_name='商品数量')),
            ],
            options={
                'verbose_name_plural': '商品信息',
                'db_table': 'tb_cart',
            },
        ),
    ]