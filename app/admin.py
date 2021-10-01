from django.contrib import admin
from .models import CustomUser, SessionYearModel, Courses, Students, Subjects, AttendanceReport, LeaveReportStudent, \
    FeedBackStudent

# Register your models here.


admin.site.register(CustomUser)


# admin.site.register(SessionYearModel)
# admin.site.register(Courses)
# admin.site.register(Students)
# admin.site.register(Subjects)
# admin.site.register(AttendanceReport)
# admin.site.register(LeaveReportStudent)
# admin.site.register(FeedBackStudent)


@admin.register(Students)
class StudentsAdmin(admin.ModelAdmin):
    list_display = ['id', 'admin', 'gender', 'profile_pic', 'address', 'course_id', 'session_year_id', 'created_at',
                    'updated_at']


@admin.register(Courses)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['id', 'course_name', 'created_at', 'updated_at']


@admin.register(LeaveReportStudent)
class LeaveReportStudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'student_id', 'leave_date', 'leave_message', 'created_at', 'updated_at']


@admin.register(FeedBackStudent)
class FeedBackStudentAdmin(admin.ModelAdmin):
    list_display = ['id', 'student_id', 'staff_id', 'user_type', 'feedback', 'created_at', 'updated_at']


@admin.register(AttendanceReport)
class AttendanceReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'student_id', 'status', 'attendance_date', 'created_at', 'updated_at']


@admin.register(SessionYearModel)
class SessionYearAdmin(admin.ModelAdmin):
    list_display = ['id', 'session_start_year', 'session_end_year']


@admin.register(Subjects)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['id', 'subject_name', 'staff_id', 'course_id', 'created_at', 'updated_at']
