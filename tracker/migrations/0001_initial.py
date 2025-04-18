# Generated by Django 4.2.10 on 2024-05-11 10:10

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('student_id', models.CharField(default='', max_length=200, unique=True)),
                ('priority_level', models.IntegerField(default=1)),
                ('first_name', models.CharField(default='', max_length=200)),
                ('last_name', models.CharField(default='', max_length=200)),
                ('username', models.CharField(default='', max_length=200)),
                ('student_deg_prog', models.CharField(max_length=200)),
                ('batch', models.CharField(default='2020', max_length=4)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='College',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('college_name', models.CharField(default='', max_length=200)),
                ('college_abbrev', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_code', models.CharField(max_length=200)),
                ('course_title', models.CharField(max_length=200)),
                ('course_description', models.CharField(default='', max_length=450)),
                ('demand', models.IntegerField(default=0)),
                ('is_elective', models.BooleanField(default=False)),
                ('units', models.IntegerField(default=3)),
                ('can_COI', models.BooleanField(default=False)),
                ('first_prio', models.IntegerField(default=0)),
                ('second_prio', models.IntegerField(default=0)),
                ('third_prio', models.IntegerField(default=0)),
                ('fourth_prio', models.IntegerField(default=0)),
                ('college', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.college')),
            ],
        ),
        migrations.CreateModel(
            name='Semester',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('semester', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(default='', max_length=200)),
                ('subject_code', models.CharField(default='', max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Report',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('academic_year', models.CharField(max_length=9)),
                ('pdf_file', models.FileField(upload_to='reports/')),
                ('upload_time', models.CharField(default='', max_length=200)),
                ('semester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tracker.semester')),
            ],
        ),
        migrations.CreateModel(
            name='Petition',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(default='', max_length=200)),
                ('description', models.CharField(default='', max_length=250)),
                ('course', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.course')),
                ('poster', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('department_name', models.CharField(default='', max_length=200)),
                ('department_abbrev', models.CharField(default='', max_length=200)),
                ('college', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.college')),
            ],
        ),
        migrations.CreateModel(
            name='DegreeProgram',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('degree_title', models.CharField(default='', max_length=200)),
                ('degree_abbbrev', models.CharField(default='', max_length=200)),
                ('college', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.college')),
            ],
        ),
        migrations.AddField(
            model_name='course',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.department'),
        ),
        migrations.AddField(
            model_name='course',
            name='prereqs',
            field=models.ManyToManyField(blank=True, to='tracker.course'),
        ),
        migrations.AddField(
            model_name='course',
            name='sem_offered',
            field=models.ManyToManyField(blank=True, related_name='semester_subs', to='tracker.semester'),
        ),
        migrations.AddField(
            model_name='course',
            name='subject_code',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.subject'),
        ),
        migrations.AddField(
            model_name='student',
            name='deg_prog',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.degreeprogram'),
        ),
        migrations.AddField(
            model_name='student',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='student',
            name='shopping_cart',
            field=models.ManyToManyField(blank=True, related_name='students', to='tracker.course'),
        ),
        migrations.AddField(
            model_name='student',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
        migrations.AlterUniqueTogether(
            name='course',
            unique_together={('subject_code', 'course_code')},
        ),
    ]
