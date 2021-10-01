from django.shortcuts import render, HttpResponseRedirect, redirect
from .forms import SignUpUsers, StudentForm
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import SessionYearModel, Courses, Students, Subjects, AttendanceReport, LeaveReportStudent, FeedBackStudent
from django.contrib import messages
import datetime
from teacherapp.models import Staffs


# Create your views here.


def user_signup(request):
    if request.method == "POST":
        fm = SignUpUsers(request.POST)
        if fm.is_valid():
            fm.save()
            print("SUCCESS!!")
            fm = SignUpUsers()
            return render(request, 'signup.html', {'fm': fm})

    fm = SignUpUsers()
    return render(request, 'signup.html', {'fm': fm})


def login_user(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = AuthenticationForm(request=request, data=request.POST)

            if fm.is_valid():
                uname = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                print(user.user_type, '----------------user-type')
                if user is not None:
                    login(request, user)
                    user_type = user.user_type
                    print(user_type)

                    if str(user_type) == '1':
                        messages.success(request, 'Logged in successfully')
                        return redirect('admin_home')

                    elif str(user_type) == '2':
                        messages.success(request, 'Logged in successfully')
                        # return HttpResponse("Staff Login")
                        print("hello -------------------------------------")
                        return redirect('staff_home')

                    elif str(user_type) == '3':
                        print("student---------------")
                        messages.success(request, 'Logged in successfully')
                        # return HttpResponse("Student Login")
                        return HttpResponseRedirect('/studenthome/')
                    else:
                        messages.error(request, "Invalid Login!")
                        return redirect('login')

        else:
            fm = AuthenticationForm()
        return render(request, 'login.html', {'form': fm})
    else:
        return HttpResponseRedirect('/studenthome/')


def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/login/')
    else:
        return HttpResponseRedirect('/login/')


def student_home(request):
    if request.user.is_authenticated:
        student = Students.objects.get(admin=request.user)
        # print(student.course_id)
        # -------------- Extracting subjects of student
        subjects = Subjects.objects.filter(course_id=student.course_id)
        # print(subjects)
        # for x in subjects:
        #     print(x.subject_name, '----------')
        # --------------

        # --------------attendance
        attendance = AttendanceReport.objects.filter(student_id=student)
        # for x in attendance:
        #     print(x.status)
        #     print(x.attendance_date)
        # --------------
        context = {
            "subjects": subjects,
            "attendance": attendance,
        }
        return render(request, 'stuhome.html', context)
    else:
        return HttpResponseRedirect('/login/')


def student_profile(request):
    if request.user.is_authenticated:
        # ---------------- Attendance count
        student = Students.objects.get(admin=request.user)
        now = datetime.date.today()
        month_start = datetime.date(now.year, now.month, 1)
        print(month_start, now)
        print(1, now.month, now.year)
        report = AttendanceReport.objects.filter(student_id=student, attendance_date__gte=month_start,
                                                 attendance_date__lte=now)
        print(report.count())
        # ----------------
        student = Students.objects.get(admin=request.user)
        context = {
            "student": student,
            "report": report,
            "report_count": report.count(),
        }
        return render(request, 'studentprofile.html', context)
    else:
        return HttpResponseRedirect('/login/')


def student_update(request):
    if request.user.is_authenticated:
        student = Students.objects.get(admin=request.user)
        if request.method == "POST":
            gender = request.POST.get('gender')
            address = request.POST.get('address')
            image = request.FILES.get('image')
            course_no = request.POST.get('course')
            session_no = request.POST.get('session')
            session = SessionYearModel.objects.get(id=session_no)
            course = Courses.objects.get(id=course_no)
            if image is not None:
                # ----------------------------
                fs = FileSystemStorage()
                pic_obj = fs.save(image.name, image)
                # print(fs)
                file_url = fs.url(pic_obj)
                student.profile_pic = file_url
                # ----------------------------
            else:
                student.profile_pic = student.profile_pic

            student.gender = gender
            student.address = address
            student.course_id = course
            student.session_year_id = session
            student.save()
            # form = StudentForm(request.POST, instance=student)
            # form.save()
            messages.success(request, '\n Student Account Updated Successfully')
            return HttpResponseRedirect('/studentprofile/')
        else:
            fm = StudentForm(instance=student)
            session = SessionYearModel.objects.all()
            course = Courses.objects.all()
            context = {
                "form": fm,
                "years": session,
                "course": course,
                "student": student,
                "course_name": student.course_id.course_name,
                "session_year": student.session_year_id.session_start_year,
            }
            return render(request, 'studentupdate.html', context)
    else:
        return HttpResponseRedirect('/login/')


def student_leave_apply(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            student = Students.objects.get(admin=request.user)
            message = request.POST.get('leave_msg')
            leave = LeaveReportStudent.objects.create(student_id=student, leave_message=message)
            messages.success(request, '\n Applied for leave Successfully')
            return HttpResponseRedirect('/studentprofile/')
        else:
            return render(request, 'studentleave.html')
    else:
        return HttpResponseRedirect('/login/')


def student_feedback(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            student = Students.objects.get(admin=request.user)
            message = request.POST.get('feedback_msg')
            staff_id = request.POST.get('staff')
            staff = Staffs.objects.get(id=staff_id)
            print(staff_id, staff.name)
            feedback = FeedBackStudent.objects.create(student_id=student, staff_id=staff,
                                                      user_type="Student to teacher", feedback=message)
            messages.success(request, '\n Feedback Submitted')
            return HttpResponseRedirect('/studentprofile/')
        else:
            staffs = Staffs.objects.all()
            context = {
                "staffs": staffs,
            }
            return render(request, 'studentfeedback.html', context)
    else:
        return HttpResponseRedirect('/login/')
