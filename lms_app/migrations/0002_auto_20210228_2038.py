# Generated by Django 3.1.2 on 2021-02-28 16:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lms_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faculty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Faculty name')),
            ],
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='mobile_number',
            field=models.CharField(default='', max_length=20, verbose_name='Mobile Number'),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='personal_id',
            field=models.CharField(default='', max_length=11, verbose_name='Personal ID'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='first_name',
            field=models.CharField(max_length=50, verbose_name='First Name'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='gpa',
            field=models.DecimalField(decimal_places=2, max_digits=3, verbose_name='GPA'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='last_name',
            field=models.CharField(max_length=50, verbose_name='Last Name'),
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Subject name')),
                ('credit_score', models.SmallIntegerField(max_length=2, verbose_name='Credit Score')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms_app.faculty', verbose_name='Faculty')),
                ('lecturer', models.ManyToManyField(to=settings.AUTH_USER_MODEL, verbose_name='Lecturer')),
            ],
        ),
        migrations.CreateModel(
            name='LecturerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('mobile_number', models.CharField(max_length=20, verbose_name='Mobile Number')),
                ('personal_id', models.CharField(max_length=11, verbose_name='Personal ID')),
                ('faculty', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='lms_app.faculty', verbose_name='Faculty')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Student')),
            ],
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='faculty',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.PROTECT, to='lms_app.faculty', verbose_name='Faculty'),
        ),
        migrations.AddField(
            model_name='studentprofile',
            name='subject',
            field=models.ManyToManyField(default=0, to='lms_app.Subject', verbose_name='Subject'),
        ),
    ]
