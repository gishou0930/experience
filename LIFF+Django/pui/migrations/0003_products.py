# Generated by Django 3.1.2 on 2021-05-08 02:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pui', '0002_delete_products'),
    ]

    operations = [
        migrations.CreateModel(
            name='products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('kind', models.CharField(max_length=30)),
                ('products', models.CharField(max_length=30)),
                ('price', models.IntegerField()),
            ],
        ),
    ]
