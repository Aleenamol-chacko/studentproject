from django.urls import path
from .views import (
    index_view,
    login_view, register_view, logout_view,

    # dashboards
    admin_dashboard, faculty_dashboard, student_dashboard,

    # student
    student_list, add_student, edit_student, delete_student, view_student,

    # faculty
    faculty_list, add_faculty, edit_faculty, delete_faculty, view_faculty,

    # course
    course_list, add_course, edit_course, delete_course, view_course,

    # HOD
    hod_list, add_hod, edit_hod, delete_hod, view_hod,

    # department
    department_list, add_department, edit_department, delete_department, view_department,

    # batch
    batch_list, add_batch, edit_batch, delete_batch, view_batch,

    # academic year
    academic_year_list, add_academic_year, edit_academic_year, delete_academic_year, view_academic_year,

    # semester
    semester_list, add_semester, edit_semester, delete_semester, view_semester,

    # attendance
    attendance_list, add_attendance, edit_attendance, delete_attendance, view_attendance,

    # payment
    payment_list, add_payment, edit_payment, delete_payment, view_payment,

    # student result
    student_result_list, add_student_result, edit_student_result, delete_student_result, view_student_result,

    # profile management
    manage_profile
)

urlpatterns = [

    # =========================
    # INDEX PAGE
    # =========================
    path('', index_view, name='index'),

    # =========================
    # LOGIN & DASHBOARD
    # =========================
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('register/', register_view, name='register'),
    
    # ✅ FIXED DASHBOARDS
    path('admindashboard/', admin_dashboard, name='dashboard'),
    path('facultydashboard/', faculty_dashboard, name='faculty_dashboard'),
    path('studentdashboard/', student_dashboard, name='student_dashboard'),

    # =========================
    # STUDENT URLS
    # =========================
    path('student/', student_list, name='student'),
    path('student/add/', add_student, name='student_add'),
    path('student/edit/<int:id>/', edit_student, name='student_edit'),
    path('student/delete/<int:id>/', delete_student, name='student_delete'),
    path('student/view/<int:id>/', view_student, name='student_view'),

    # =========================
    # FACULTY URLS
    # =========================
    path('faculty/', faculty_list, name='faculty'),
    path('faculty/add/', add_faculty, name='faculty_add'),
    path('faculty/edit/<int:id>/', edit_faculty, name='faculty_edit'),
    path('faculty/delete/<int:id>/', delete_faculty, name='faculty_delete'),
    path('faculty/view/<int:id>/', view_faculty, name='faculty_view'),

    # =========================
    # COURSE URLS
    # =========================
    path('course/', course_list, name='course'),
    path('course/add/', add_course, name='course_add'),
    path('course/view/<int:id>/', view_course, name='course_view'),
    path('course/edit/<int:id>/', edit_course, name='course_edit'),
    path('course/delete/<int:id>/', delete_course, name='course_delete'),

    # =========================
    # HOD URLS
    # =========================
    path('hod/', hod_list, name='hod'),
    path('hod/add/', add_hod, name='hod_add'),
    path('hod/view/<int:id>/', view_hod, name='hod_view'),
    path('hod/edit/<int:id>/', edit_hod, name='hod_edit'),
    path('hod/delete/<int:id>/', delete_hod, name='hod_delete'),

    # =========================
    # DEPARTMENT URLS
    # =========================
    path('department/', department_list, name='department'),
    path('department/add/', add_department, name='department_add'),
    path('department/view/<int:id>/', view_department, name='department_view'),
    path('department/edit/<int:id>/', edit_department, name='department_edit'),
    path('department/delete/<int:id>/', delete_department, name='department_delete'),

    # =========================
    # BATCH URLS
    # =========================
    path('batch/', batch_list, name='batch'),
    path('batch/add/', add_batch, name='batch_add'),
    path('batch/view/<int:id>/', view_batch, name='batch_view'),
    path('batch/edit/<int:id>/', edit_batch, name='batch_edit'),
    path('batch/delete/<int:id>/', delete_batch, name='batch_delete'),

    # =========================
    # ACADEMIC YEAR URLS
    # =========================
    path('academic-year/', academic_year_list, name='academic_year'),
    path('academic-year/add/', add_academic_year, name='academic_year_add'),
    path('academic-year/view/<int:id>/', view_academic_year, name='academic_year_view'),
    path('academic-year/edit/<int:id>/', edit_academic_year, name='academic_year_edit'),
    path('academic-year/delete/<int:id>/', delete_academic_year, name='academic_year_delete'),

    # =========================
    # SEMESTER URLS
    # =========================
    path('semester/', semester_list, name='semester'),
    path('semester/add/', add_semester, name='semester_add'),
    path('semester/view/<int:id>/', view_semester, name='semester_view'),
    path('semester/edit/<int:id>/', edit_semester, name='semester_edit'),
    path('semester/delete/<int:id>/', delete_semester, name='semester_delete'),

    # =========================
    # ATTENDANCE URLS
    # =========================
    path('attendance/', attendance_list, name='attendance'),
    path('attendance/add/', add_attendance, name='attendance_add'),
    path('attendance/view/<int:id>/', view_attendance, name='attendance_view'),
    path('attendance/edit/<int:id>/', edit_attendance, name='attendance_edit'),
    path('attendance/delete/<int:id>/', delete_attendance, name='attendance_delete'),

    # =========================
    # PAYMENT URLS
    # =========================
    path('payment/', payment_list, name='payment'),
    path('payment/add/', add_payment, name='payment_add'),
    path('payment/view/<int:id>/', view_payment, name='payment_view'),
    path('payment/edit/<int:id>/', edit_payment, name='payment_edit'),
    path('payment/delete/<int:id>/', delete_payment, name='payment_delete'),

    # =========================
    # STUDENT RESULT URLS
    # =========================
    path('student-result/', student_result_list, name='student_result'),
    path('student-result/add/', add_student_result, name='student_result_add'),
    path('student-result/view/<int:id>/', view_student_result, name='student_result_view'),
    path('student-result/edit/<int:id>/', edit_student_result, name='student_result_edit'),
    path('student-result/delete/<int:id>/', delete_student_result, name='student_result_delete'),

    # =========================
    # PROFILE MANAGEMENT
    # =========================
    path('manage-profile/', manage_profile, name='manage_profile'),
]