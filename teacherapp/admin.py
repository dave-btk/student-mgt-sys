from django.contrib import admin
from .models import Staffs, AttendanceReportStaff, LeaveReportStaff


# Register your models here.


@admin.register(Staffs)
class StaffAdmin(admin.ModelAdmin):
    list_display = ['id', 'admin', 'name', 'role', 'address', 'created_at', 'updated_at']


@admin.register(AttendanceReportStaff)
class AttendanceReportStaffAdmin(admin.ModelAdmin):
    list_display = ['id', 'staff_id', 'status', 'attendance_date', 'created_at', 'updated_at']


@admin.register(LeaveReportStaff)
class AttendanceReportStaffAdmin(admin.ModelAdmin):
    list_display = ['id', 'staff_id', 'leave_date', 'leave_message', 'created_at', 'updated_at']
