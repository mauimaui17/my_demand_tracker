# Generated by Django 4.2.10 on 2024-05-11 12:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0003_report_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='report',
            name='pdf_file',
            field=models.FileField(upload_to=''),
        ),
    ]
