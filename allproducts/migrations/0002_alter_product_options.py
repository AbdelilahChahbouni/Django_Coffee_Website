# Generated by Django 4.2.2 on 2023-06-20 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('allproducts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-puplish_date']},
        ),
    ]
