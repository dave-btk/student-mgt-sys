from django.shortcuts import render, HttpResponseRedirect, redirect
from .models import Staffs, AttendanceReportStaff, LeaveReportStaff
from django.contrib import messages
from app.models import Subjects, Students, FeedBackStudent
import datetime


# Create your views here.

def staff_home(request):
    staff = Staffs.objects.get(admin=request.user)
    subjects = Subjects.objects.filter(staff_id=staff)
    # ----------------
    names = {}
    for subject in subjects:
        print(subject.subject_name, '------------------start')
        print(subject.course_id, '-----------------course-id')
        students = Students.objects.filter(course_id=subject.course_id)
        list = []

        for student in students:
            list.append(str(student.admin))
            print(list)
        print(list)
        names[f"{subject.course_id}"] = list
        print(names, '--------end')

    print(names, '--------------final')
    # res = []
    # for x in list:
    #     if x not in res:
    #         res.append(x)
    #
    # print(res, 'new-------')

    context = {
        "student_names": names
    }
    return render(request, 'staffhome.html', context)


def staff_profile(request):
    if request.user.is_authenticated:
        # ---------------- Attendance count
        staff = Staffs.objects.get(admin=request.user)
        now = datetime.date.today()
        month_start = datetime.date(now.year, now.month, 1)
        print(month_start, now)
        print(1, now.month, now.year)
        report = AttendanceReportStaff.objects.filter(staff_id=staff, attendance_date__gte=month_start,
                                                      attendance_date__lte=now)
        print(report.count())
        # ----------------
        staff = Staffs.objects.get(admin=request.user)
        context = {
            "staff": staff,
            "report": report,
            "report_count": report.count(),
        }
        return render(request, 'staffprofile.html', context)
    else:
        return HttpResponseRedirect('/login/')


def staff_update(request):
    if request.user.is_authenticated:
        staff = Staffs.objects.get(admin=request.user)
        if request.method == "POST":
            name = request.POST.get('name')
            role = request.POST.get('role')
            address = request.POST.get('address')
            staff.name = name
            staff.role = role
            staff.address = address
            staff.save()
            messages.success(request, '\n Student Account Updated Successfully')
            return HttpResponseRedirect('/staffprofile/')
        else:
            print(staff.address)
            context = {
                "staff": staff
            }
        return render(request, 'staffupdate.html', context)
    else:
        return HttpResponseRedirect('/login/')


def staff_feedback(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            message = request.POST.get('feedback_msg')
            student_id = request.POST.get('students')
            student = Students.objects.get(id=student_id)
            staff = Staffs.objects.get(admin=request.user)
            print(student_id, student.admin)
            feedback = FeedBackStudent.objects.create(student_id=student, staff_id=staff,
                                                      user_type="Teacher to Student", feedback=message)
            messages.success(request, '\n Feedback Submitted')
            return HttpResponseRedirect('/staffprofile/')
        else:
            students = Students.objects.all()
            context = {
                "students": students,
            }
            return render(request, 'stafffeedback.html', context)
    else:
        return HttpResponseRedirect('/login/')


def staff_leave_apply(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            staffs = Staffs.objects.get(admin=request.user)
            message = request.POST.get('leave_msg')
            leave = LeaveReportStaff.objects.create(staff_id=staffs, leave_message=message)
            messages.success(request, '\n Applied for leave Successfully')
            return HttpResponseRedirect('/staffprofile/')
        else:
            return render(request, 'staffleave.html')
    else:
        return HttpResponseRedirect('/login/')
