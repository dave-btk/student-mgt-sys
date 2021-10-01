from django.db import models
from app.models import CustomUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
import datetime


# Create your models here.


class Staffs(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.TextField(max_length=50)
    role = models.TextField(max_length=200)
    address = models.TextField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# ----------------------------

class AttendanceReportStaff(models.Model):
    # Individual Staff Attendance
    staff_id = models.ForeignKey(Staffs, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=False)
    attendance_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# ----------------------------


class LeaveReportStaff(models.Model):
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    leave_date = models.DateTimeField(auto_now_add=True)
    leave_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class NotificationStaffs(models.Model):
    staff_id = models.ForeignKey(Staffs, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        if instance.user_type == 2:
            Staffs.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    if instance.user_type == 2:
        instance.staffs.save()


@receiver(user_logged_in, sender=CustomUser)
def user_login(sender, request, user, **kwargs):
    if request.user.user_type == 2:
        print(request.user.user_type, "here user-type")
        staff = Staffs.objects.get(admin=request.user)
        attendance = AttendanceReportStaff.objects.filter(staff_id=staff,
                                                          attendance_date__gte=datetime.date.today()).first()

        if attendance is None:
            attendance = AttendanceReportStaff.objects.create(
                staff_id=staff,
                status=True,
            )
            print("attendance marked")
        else:
            print(attendance.attendance_date, attendance)
            print("already marked")
