# Generated by Django 4.1 on 2023-07-03 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_address_options_remove_product_tags_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='category', to='core.category'),
        ),
    ]
