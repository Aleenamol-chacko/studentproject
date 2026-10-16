from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Student, Faculty, Course, Department, Batch, AcademicYear, Semester, HOD, Attendance, Payment, StudentResult


# =========================
# INDEX PAGE
# =========================
def index_view(request):
    return render(request, 'index.html')


# =========================
# LOGIN
# =========================
def login_view(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # ✅ ROLE CHECK
            if user.is_superuser:
                return redirect('dashboard')

            elif user.groups.filter(name='Faculty').exists():
                return redirect('faculty_dashboard')

            elif user.groups.filter(name='Student').exists():
                return redirect('student_dashboard')

            else:
                return redirect('dashboard')

        else:
            return render(request, "login.html", {"error": "Invalid login"})

    return render(request, "login.html")


# =========================
# REGISTRATION
# =========================
def register_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        
        # Basic validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request, "register.html")
        
        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered")
            return render(request, "register.html")
        
        # Create user
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )
        
        messages.success(request, "Registration successful! Please login.")
        return redirect('login')
    
    return render(request, "register.html")


# =========================
# LOGOUT
# =========================
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('login')


# =========================
# DASHBOARDS
# =========================
@login_required
def admin_dashboard(request):
    return render(request, "admindashboard.html")


@login_required
def faculty_dashboard(request):
    return render(request, "facultydashboard.html")


@login_required
def student_dashboard(request):
    return render(request, "studentdashboard.html")


# =========================
# STUDENT MODULE
# =========================
@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, "studentmanagement.html", {"students": students})


@login_required
def add_student(request):
    if request.method == "POST":
        Student.objects.create(
            fullname=request.POST.get("fullname"),
            dob=request.POST.get("dob") or None,
            gender=request.POST.get("gender"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            qualification=request.POST.get("qualification"),
            bloodGrp=request.POST.get("bloodGrp"),
            studentid=request.POST.get("studentid") or None,
            department=request.POST.get("department"),
            year=request.POST.get("year"),
            admissiondate=request.POST.get("admissiondate") or None,
            cgpa=request.POST.get("cgpa") or 0,
            address=request.POST.get("address"),
            city=request.POST.get("city"),
            photo=request.FILES.get("photo"),
            id_proof=request.FILES.get("id_proof")
        )
        return redirect("student")   # ✅ FIXED

    return render(request, "addstudent.html")


@login_required
def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.fullname = request.POST.get("fullname")
        student.dob = request.POST.get("dob") or None
        student.gender = request.POST.get("gender")
        student.email = request.POST.get("email")
        student.phone = request.POST.get("phone")
        student.qualification = request.POST.get("qualification")
        student.bloodGrp = request.POST.get("bloodGrp")
        student.studentid = request.POST.get("studentid") or student.studentid
        student.department = request.POST.get("department")
        student.year = request.POST.get("year")
        student.admissiondate = request.POST.get("admissiondate") or None
        student.cgpa = request.POST.get("cgpa") or 0
        student.address = request.POST.get("address")
        student.city = request.POST.get("city")

        if request.FILES.get("photo"):
            student.photo = request.FILES.get("photo")

        if request.FILES.get("id_proof"):
            student.id_proof = request.FILES.get("id_proof")

        student.save()
        return redirect("student")

    return render(request, "editstudent.html", {"student": student})


@login_required
def delete_student(request, id):
    student = get_object_or_404(Student, id=id)
    student.delete()
    return redirect("student")


@login_required
def view_student(request, id):
    student = get_object_or_404(Student, id=id)
    return render(request, "viewstudent.html", {"student": student})


# =========================
# FACULTY MODULE
# =========================
@login_required
def faculty_list(request):
    faculty = Faculty.objects.all()
    return render(request, "facultymanagement.html", {"faculty": faculty})


@login_required
def add_faculty(request):
    if request.method == "POST":
        Faculty.objects.create(
            fullname=request.POST.get("fullname"),
            dob=request.POST.get("dob") or None,
            gender=request.POST.get("gender"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            department=request.POST.get("department"),
            designation=request.POST.get("designation"),
            qualification=request.POST.get("qualification"),
            experience=request.POST.get("experience") or 0,
            joining_date=request.POST.get("joining_date") or None,
            address=request.POST.get("address"),
            city=request.POST.get("city")
        )
        return redirect("faculty")

    return render(request, "addfaculty.html")


@login_required
def edit_faculty(request, id):
    faculty = get_object_or_404(Faculty, id=id)

    if request.method == "POST":
        faculty.fullname = request.POST.get("fullname")
        faculty.dob = request.POST.get("dob") or None
        faculty.gender = request.POST.get("gender")
        faculty.email = request.POST.get("email")
        faculty.phone = request.POST.get("phone")
        faculty.department = request.POST.get("department")
        faculty.designation = request.POST.get("designation")
        faculty.joining_date = request.POST.get("joining_date") or None
        faculty.qualification = request.POST.get("qualification")
        faculty.experience = request.POST.get("experience") or 0
        faculty.address = request.POST.get("address")
        faculty.city = request.POST.get("city")

        if request.FILES.get("photo"):
            faculty.photo = request.FILES.get("photo")

        if request.FILES.get("id_proof"):
            faculty.id_proof = request.FILES.get("id_proof")

        faculty.save()
        return redirect("faculty")

    return render(request, "editfaculty.html", {"faculty": faculty})


@login_required
def delete_faculty(request, id):
    faculty = get_object_or_404(Faculty, id=id)
    faculty.delete()
    return redirect("faculty")


@login_required
def view_faculty(request, id):
    faculty = get_object_or_404(Faculty, id=id)
    return render(request, "viewfaculty.html", {"faculty": faculty})


# =========================
# COURSE MODULE
# =========================
@login_required
def course_list(request):
    courses = Course.objects.all()
    return render(request, "coursemanagement.html", {"courses": courses})


@login_required
def add_course(request):
    if request.method == "POST":
        Course.objects.create(
            coursename=request.POST.get("coursename"),
            department=request.POST.get("department"),
            credits=request.POST.get("credits") or 0,
            semester=request.POST.get("semester"),
            duration=request.POST.get("duration"),
            course_description=request.POST.get("course_description", "")
        )
        return redirect("course")

    return render(request, "addcourse.html")


@login_required
def view_course(request, id):
    course = get_object_or_404(Course, id=id)
    return render(request, "viewcourse.html", {"course": course})


@login_required
def edit_course(request, id):
    course = get_object_or_404(Course, id=id)

    if request.method == "POST":
        course.coursename = request.POST.get("coursename")
        course.department = request.POST.get("department")
        course.credits = request.POST.get("credits") or 0
        course.semester = request.POST.get("semester")
        course.duration = request.POST.get("duration")
        course.course_description = request.POST.get("course_description", "")
        course.save()

        return redirect("course")

    return render(request, "editcourse.html", {"course": course})


@login_required
def delete_course(request, id):
    course = get_object_or_404(Course, id=id)
    course.delete()
    return redirect("course")


# =========================
# HOD MANAGEMENT
# =========================
@login_required
def hod_list(request):
    hods = HOD.objects.select_related('department', 'user').all()
    return render(request, "hodmanagement.html", {"hods": hods})

@login_required
def add_hod(request):
    if request.method == "POST":
        user = User.objects.create_user(
            username=request.POST.get("email"),
            email=request.POST.get("email"),
            password=request.POST.get("password"),
            first_name=request.POST.get("name")
        )
        department = get_object_or_404(Department, id=request.POST.get("department"))
        HOD.objects.create(
            user=user,
            department=department,
            phone=request.POST.get("phone"),
            office_location=request.POST.get("office_location"),
            joining_date=request.POST.get("joining_date")
        )
        return redirect("hod")
    departments = Department.objects.all()
    return render(request, "addhod.html", {"departments": departments})

@login_required
def edit_hod(request, id):
    hod = get_object_or_404(HOD, id=id)
    if request.method == "POST":
        hod.phone = request.POST.get("phone")
        hod.office_location = request.POST.get("office_location")
        hod.joining_date = request.POST.get("joining_date")
        if request.POST.get("department"):
            hod.department = get_object_or_404(Department, id=request.POST.get("department"))
        hod.save()
        return redirect("hod")
    departments = Department.objects.all()
    return render(request, "edithod.html", {"hod": hod, "departments": departments})

@login_required
def delete_hod(request, id):
    hod = get_object_or_404(HOD, id=id)
    hod.delete()
    return redirect("hod")


# =========================
# DEPARTMENT MANAGEMENT
# =========================
@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, "departmentmanagement.html", {"departments": departments})

@login_required
def add_department(request):
    if request.method == "POST":
        Department.objects.create(
            name=request.POST.get("name"),
            code=request.POST.get("code"),
            hod=request.POST.get("hod"),
            description=request.POST.get("description")
        )
        return redirect("department")
    return render(request, "adddepartment.html")

@login_required
def edit_department(request, id):
    department = get_object_or_404(Department, id=id)
    if request.method == "POST":
        department.name = request.POST.get("name")
        department.code = request.POST.get("code")
        department.hod = request.POST.get("hod")
        department.description = request.POST.get("description")
        department.save()
        return redirect("department")
    return render(request, "editdepartment.html", {"department": department})

@login_required
def delete_department(request, id):
    department = get_object_or_404(Department, id=id)
    department.delete()
    return redirect("department")


# =========================
# BATCH MANAGEMENT
# =========================
@login_required
def batch_list(request):
    batches = Batch.objects.select_related('department').all()
    return render(request, "batchmanagement.html", {"batches": batches})

@login_required
def add_batch(request):
    if request.method == "POST":
        Batch.objects.create(
            name=request.POST.get("name"),
            year=request.POST.get("year"),
            department=get_object_or_404(Department, id=request.POST.get("department")),
            start_date=request.POST.get("start_date"),
            end_date=request.POST.get("end_date"),
            is_active=request.POST.get("is_active") == 'on'
        )
        return redirect("batch")
    departments = Department.objects.all()
    return render(request, "addbatch.html", {"departments": departments})

@login_required
def edit_batch(request, id):
    batch = get_object_or_404(Batch, id=id)
    if request.method == "POST":
        batch.name = request.POST.get("name")
        batch.year = request.POST.get("year")
        batch.department = get_object_or_404(Department, id=request.POST.get("department"))
        batch.start_date = request.POST.get("start_date")
        batch.end_date = request.POST.get("end_date")
        batch.is_active = request.POST.get("is_active") == 'on'
        batch.save()
        return redirect("batch")
    departments = Department.objects.all()
    return render(request, "editbatch.html", {"batch": batch, "departments": departments})

@login_required
def delete_batch(request, id):
    batch = get_object_or_404(Batch, id=id)
    batch.delete()
    return redirect("batch")


# =========================
# ACADEMIC YEAR MANAGEMENT
# =========================
@login_required
def academic_year_list(request):
    academic_years = AcademicYear.objects.all()
    return render(request, "academicyearmanagement.html", {"academic_years": academic_years})

@login_required
def add_academic_year(request):
    if request.method == "POST":
        AcademicYear.objects.create(
            name=request.POST.get("name"),
            start_date=request.POST.get("start_date"),
            end_date=request.POST.get("end_date"),
            is_current=request.POST.get("is_current") == 'on'
        )
        return redirect("academic_year")
    return render(request, "addacademicyear.html")

@login_required
def edit_academic_year(request, id):
    academic_year = get_object_or_404(AcademicYear, id=id)
    if request.method == "POST":
        academic_year.name = request.POST.get("name")
        academic_year.start_date = request.POST.get("start_date")
        academic_year.end_date = request.POST.get("end_date")
        academic_year.is_current = request.POST.get("is_current") == 'on'
        academic_year.save()
        return redirect("academic_year")
    return render(request, "editacademicyear.html", {"academic_year": academic_year})

@login_required
def delete_academic_year(request, id):
    academic_year = get_object_or_404(AcademicYear, id=id)
    academic_year.delete()
    return redirect("academic_year")


# =========================
# SEMESTER MANAGEMENT
# =========================
@login_required
def semester_list(request):
    semesters = Semester.objects.select_related('academic_year').all()
    return render(request, "semestermanagement.html", {"semesters": semesters})

@login_required
def add_semester(request):
    if request.method == "POST":
        Semester.objects.create(
            name=request.POST.get("name"),
            academic_year=get_object_or_404(AcademicYear, id=request.POST.get("academic_year")),
            semester_number=request.POST.get("semester_number"),
            start_date=request.POST.get("start_date"),
            end_date=request.POST.get("end_date"),
            is_active=request.POST.get("is_active") == 'on'
        )
        return redirect("semester")
    academic_years = AcademicYear.objects.all()
    return render(request, "addsemester.html", {"academic_years": academic_years})

@login_required
def edit_semester(request, id):
    semester = get_object_or_404(Semester, id=id)
    if request.method == "POST":
        semester.name = request.POST.get("name")
        semester.academic_year = get_object_or_404(AcademicYear, id=request.POST.get("academic_year"))
        semester.semester_number = request.POST.get("semester_number")
        semester.start_date = request.POST.get("start_date")
        semester.end_date = request.POST.get("end_date")
        semester.is_active = request.POST.get("is_active") == 'on'
        semester.save()
        return redirect("semester")
    academic_years = AcademicYear.objects.all()
    return render(request, "editsemester.html", {"semester": semester, "academic_years": academic_years})

@login_required
def delete_semester(request, id):
    semester = get_object_or_404(Semester, id=id)
    semester.delete()
    return redirect("semester")


# =========================
# ATTENDANCE MANAGEMENT
# =========================
@login_required
def attendance_list(request):
    attendances = Attendance.objects.select_related('student', 'course', 'marked_by', 'semester').all()
    return render(request, "attendancemanagement.html", {"attendances": attendances})

@login_required
def add_attendance(request):
    if request.method == "POST":
        Attendance.objects.create(
            student=get_object_or_404(Student, id=request.POST.get("student")),
            course=get_object_or_404(Course, id=request.POST.get("course")),
            date=request.POST.get("date"),
            status=request.POST.get("status"),
            marked_by=get_object_or_404(Faculty, id=request.POST.get("marked_by")),
            semester=get_object_or_404(Semester, id=request.POST.get("semester"))
        )
        return redirect("attendance")
    students = Student.objects.all()
    courses = Course.objects.all()
    faculties = Faculty.objects.all()
    semesters = Semester.objects.all()
    return render(request, "addattendance.html", {
        "students": students,
        "courses": courses,
        "faculties": faculties,
        "semesters": semesters
    })

@login_required
def edit_attendance(request, id):
    attendance = get_object_or_404(Attendance, id=id)
    if request.method == "POST":
        attendance.student = get_object_or_404(Student, id=request.POST.get("student"))
        attendance.course = get_object_or_404(Course, id=request.POST.get("course"))
        attendance.date = request.POST.get("date")
        attendance.status = request.POST.get("status")
        attendance.marked_by = get_object_or_404(Faculty, id=request.POST.get("marked_by"))
        attendance.semester = get_object_or_404(Semester, id=request.POST.get("semester"))
        attendance.save()
        return redirect("attendance")
    students = Student.objects.all()
    courses = Course.objects.all()
    faculties = Faculty.objects.all()
    semesters = Semester.objects.all()
    return render(request, "editattendance.html", {
        "attendance": attendance,
        "students": students,
        "courses": courses,
        "faculties": faculties,
        "semesters": semesters
    })

@login_required
def delete_attendance(request, id):
    attendance = get_object_or_404(Attendance, id=id)
    attendance.delete()
    return redirect("attendance")


# =========================
# PAYMENT MANAGEMENT
# =========================
@login_required
def payment_list(request):
    payments = Payment.objects.select_related('student').all()
    return render(request, "paymentmanagement.html", {"payments": payments})

@login_required
def add_payment(request):
    if request.method == "POST":
        Payment.objects.create(
            student=get_object_or_404(Student, id=request.POST.get("student")),
            amount=request.POST.get("amount"),
            payment_type=request.POST.get("payment_type"),
            payment_method=request.POST.get("payment_method"),
            status=request.POST.get("status"),
            transaction_id=request.POST.get("transaction_id"),
            description=request.POST.get("description")
        )
        return redirect("payment")
    students = Student.objects.all()
    return render(request, "addpayment.html", {"students": students})

@login_required
def edit_payment(request, id):
    payment = get_object_or_404(Payment, id=id)
    if request.method == "POST":
        payment.student = get_object_or_404(Student, id=request.POST.get("student"))
        payment.amount = request.POST.get("amount")
        payment.payment_type = request.POST.get("payment_type")
        payment.payment_method = request.POST.get("payment_method")
        payment.status = request.POST.get("status")
        payment.transaction_id = request.POST.get("transaction_id")
        payment.description = request.POST.get("description")
        payment.save()
        return redirect("payment")
    students = Student.objects.all()
    return render(request, "editpayment.html", {"payment": payment, "students": students})

@login_required
def delete_payment(request, id):
    payment = get_object_or_404(Payment, id=id)
    payment.delete()
    return redirect("payment")


# =========================
# STUDENT RESULT MANAGEMENT
# =========================
@login_required
def student_result_list(request):
    results = StudentResult.objects.select_related('student', 'course', 'semester').all()
    return render(request, "studentresultmanagement.html", {"results": results})

@login_required
def add_student_result(request):
    if request.method == "POST":
        StudentResult.objects.create(
            student=get_object_or_404(Student, id=request.POST.get("student")),
            course=get_object_or_404(Course, id=request.POST.get("course")),
            semester=get_object_or_404(Semester, id=request.POST.get("semester")),
            internal_marks=request.POST.get("internal_marks"),
            external_marks=request.POST.get("external_marks")
        )
        return redirect("student_result")
    students = Student.objects.all()
    courses = Course.objects.all()
    semesters = Semester.objects.all()
    return render(request, "addstudentresult.html", {
        "students": students,
        "courses": courses,
        "semesters": semesters
    })

@login_required
def edit_student_result(request, id):
    result = get_object_or_404(StudentResult, id=id)
    if request.method == "POST":
        result.student = get_object_or_404(Student, id=request.POST.get("student"))
        result.course = get_object_or_404(Course, id=request.POST.get("course"))
        result.semester = get_object_or_404(Semester, id=request.POST.get("semester"))
        result.internal_marks = request.POST.get("internal_marks")
        result.external_marks = request.POST.get("external_marks")
        result.save()
        return redirect("student_result")
    students = Student.objects.all()
    courses = Course.objects.all()
    semesters = Semester.objects.all()
    return render(request, "editstudentresult.html", {
        "result": result,
        "students": students,
        "courses": courses,
        "semesters": semesters
    })

@login_required
def delete_student_result(request, id):
    result = get_object_or_404(StudentResult, id=id)
    result.delete()
    return redirect("student_result")


# =========================
# MISSING VIEW FUNCTIONS
# =========================

@login_required
def view_hod(request, id):
    hod = get_object_or_404(HOD, id=id)
    return render(request, "viewhod.html", {"hod": hod})

@login_required
def view_department(request, id):
    department = get_object_or_404(Department, id=id)
    return render(request, "viewdepartment.html", {"department": department})

@login_required
def view_batch(request, id):
    batch = get_object_or_404(Batch, id=id)
    return render(request, "viewbatch.html", {"batch": batch})

@login_required
def view_academic_year(request, id):
    academic_year = get_object_or_404(AcademicYear, id=id)
    return render(request, "viewacademicyear.html", {"academic_year": academic_year})

@login_required
def view_semester(request, id):
    semester = get_object_or_404(Semester, id=id)
    return render(request, "viewsemester.html", {"semester": semester})

@login_required
def view_attendance(request, id):
    attendance = get_object_or_404(Attendance, id=id)
    return render(request, "viewattendance.html", {"attendance": attendance})

@login_required
def view_payment(request, id):
    payment = get_object_or_404(Payment, id=id)
    return render(request, "viewpayment.html", {"payment": payment})

@login_required
def view_student_result(request, id):
    result = get_object_or_404(StudentResult, id=id)
    return render(request, "viewstudentresult.html", {"result": result})

@login_required
def manage_profile(request):
    if request.method == "POST":
        user = request.user
        user.first_name = request.POST.get('first_name', user.first_name)
        user.last_name = request.POST.get('last_name', user.last_name)
        user.email = request.POST.get('email', user.email)
        if request.POST.get('password'):
            user.set_password(request.POST.get('password'))
        user.save()
        return redirect('dashboard')
    
    return render(request, "manageprofile.html", {"user": request.user})