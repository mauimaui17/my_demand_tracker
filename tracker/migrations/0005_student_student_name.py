# Generated by Django 4.2.10 on 2024-04-04 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_remove_student_student_name_alter_student_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='student_name',
            field=models.CharField(default='', max_length=200),
        ),
    ]
