# Generated by Django 5.0 on 2024-01-01 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advertiser_mangement', '0003_alter_click_clicker_ip_alter_view_viewer_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='click',
            name='clicker_ip',
            field=models.GenericIPAddressField(),
        ),
        migrations.AlterField(
            model_name='view',
            name='viewer_ip',
            field=models.GenericIPAddressField(),
        ),
    ]
