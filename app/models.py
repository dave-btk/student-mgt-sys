from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in
import datetime


# Create your models here.


class CustomUser(AbstractUser):
    user_type_data = ((1, "HOD"), (2, "Staff"), (3, "Student"))
    user_type = models.IntegerField(default=1, choices=user_type_data, max_length=10)


class SessionYearModel(models.Model):
    session_start_year = models.DateField()
    session_end_year = models.DateField()


class Courses(models.Model):
    course_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Students(models.Model):
    admin = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    gender = models.CharField(max_length=50)
    profile_pic = models.TextField(default=1)
    address = models.TextField()
    course_id = models.ForeignKey(Courses, on_delete=models.DO_NOTHING, default=1)
    session_year_id = models.ForeignKey(SessionYearModel, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()


class Subjects(models.Model):
    subject_name = models.CharField(max_length=255)
    course_id = models.ForeignKey(Courses, on_delete=models.CASCADE, default=1)  # need to give defauult course
    created_at = models.DateTimeField(auto_now_add=True)
    staff_id = models.ForeignKey('teacherapp.Staffs', on_delete=models.CASCADE, default=1)
    updated_at = models.DateTimeField(auto_now=True)


# ----------------------------

class AttendanceReport(models.Model):
    # Individual Student Attendance
    student_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING)
    status = models.BooleanField(default=False)
    attendance_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

# ----------------------------


class LeaveReportStudent(models.Model):
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    leave_date = models.DateTimeField(auto_now_add=True)
    leave_message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class FeedBackStudent(models.Model):
    student_id = models.ForeignKey(Students, on_delete=models.CASCADE)
    staff_id = models.ForeignKey('teacherapp.Staffs', on_delete=models.CASCADE)
    user_type = models.TextField(max_length=30)
    feedback = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


@receiver(post_save, sender=CustomUser)
# Now Creating a Function which will automatically insert data in HOD, Staff or Student
def create_user_profile(sender, instance, created, **kwargs):
    # if Created is true (Means Data Inserted)
    if created:
        # Check the user_type and insert the data in respective tables
        # if instance.user_type == 1:
        #     AdminHOD.objects.create(admin=instance)
        # if instance.user_type == 2:
        #     Staffs.objects.create(admin=instance)
        if instance.user_type == 3:
            Students.objects.create(admin=instance)


@receiver(post_save, sender=CustomUser)
def save_user_profile(sender, instance, **kwargs):
    # if instance.user_type == 1:
    #     instance.adminhod.save()
    # if instance.user_type == 2:
    #     instance.staffs.save()
    if instance.user_type == 3:
        instance.students.save()


@receiver(user_logged_in, sender=CustomUser)
def user_login(sender, request, user, **kwargs):
    if request.user.user_type == 2:
        print("staff attendance")
    if request.user.user_type == 3:
        print(request.user.user_type, "here user-type")
        students = Students.objects.get(admin=request.user)
        attendance = AttendanceReport.objects.filter(student_id=students,
                                                     attendance_date__gte=datetime.date.today()).first()

        if attendance is None:
            attendance = AttendanceReport.objects.create(
                student_id=students,
                status=True,
            )
            print("attendance marked")
        else:
            print(attendance.attendance_date, attendance)
            print("already marked")
