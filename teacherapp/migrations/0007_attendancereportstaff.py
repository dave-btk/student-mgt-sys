# Generated by Django 3.2.7 on 2021-09-28 12:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacherapp', '0006_feedbackstaffs_leavereportstaff_notificationstaffs'),
    ]

    operations = [
        migrations.CreateModel(
            name='AttendanceReportStaff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.BooleanField(default=False)),
                ('attendance_date', models.DateField(auto_now_add=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('staff_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='teacherapp.staffs')),
            ],
        ),
    ]
