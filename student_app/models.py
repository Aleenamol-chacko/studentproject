from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# =========================
# STUDENT MODEL
# =========================
class Student(models.Model):

    studentid = models.CharField(max_length=100, unique=True, blank=True)

    fullname = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    email = models.EmailField()
    phone = models.CharField(max_length=15)

    bloodGrp = models.CharField(max_length=5)  # FIX: allow values like O+
    department = models.CharField(max_length=100)
    year = models.CharField(max_length=20)
    admissiondate = models.DateField()

    qualification = models.CharField(max_length=50)
    cgpa = models.FloatField()

    address = models.TextField()
    city = models.CharField(max_length=100)  # FIX: better than TextField

    photo = models.ImageField(upload_to="student_photos/", null=True, blank=True)
    id_proof = models.FileField(upload_to="student_documents/", blank=True, null=True)

    def __str__(self):
        return self.fullname

    def save(self, *args, **kwargs):
        if not self.studentid:
            now = datetime.now().strftime("%Y%m%d%H%M%S")
            self.studentid = f"REG{now}"
        super().save(*args, **kwargs)


# =========================
# FACULTY MODEL
# =========================
class Faculty(models.Model):

    facultyid = models.CharField(max_length=100, unique=True, blank=True)

    fullname = models.CharField(max_length=100)
    dob = models.DateField()
    gender = models.CharField(max_length=10)

    email = models.EmailField()
    phone = models.CharField(max_length=15)

    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)

    qualification = models.CharField(max_length=100)
    experience = models.IntegerField()

    joining_date = models.DateField(null=True, blank=True)

    address = models.TextField()
    city = models.CharField(max_length=100, null=True, blank=True)

    photo = models.ImageField(upload_to="faculty_photos/", null=True, blank=True)
    id_proof = models.FileField(upload_to="faculty_documents/", blank=True, null=True)

    def __str__(self):
        return self.fullname

    def save(self, *args, **kwargs):
        if not self.facultyid:
            now = datetime.now().strftime("%Y%m%d%H%M%S")
            self.facultyid = f"FAC{now}"
        super().save(*args, **kwargs)


# =========================
# COURSE MODEL
# =========================
class Course(models.Model):

    courseid = models.CharField(max_length=100, unique=True, blank=True)

    coursename = models.CharField(max_length=200)
    department = models.CharField(max_length=100)
    credits = models.IntegerField()
    semester = models.CharField(max_length=20)
    duration = models.CharField(max_length=50)
    course_description = models.TextField(blank=True, null=True)

    # ✅ RELATION WITH FACULTY
    faculty = models.ForeignKey(
        Faculty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="courses"
    )

    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.coursename

    def save(self, *args, **kwargs):
        if not self.courseid:
            now = datetime.now().strftime("%Y%m%d%H%M%S")
            self.courseid = f"CRS{now}"
        super().save(*args, **kwargs)


# =========================
# DEPARTMENT MODEL
# =========================
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    hod = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


# =========================
# BATCH MODEL
# =========================
class Batch(models.Model):
    name = models.CharField(max_length=50)
    year = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.year})"


# =========================
# ACADEMIC YEAR MODEL
# =========================
class AcademicYear(models.Model):
    name = models.CharField(max_length=20, unique=True)  # e.g., "2023-2024"
    start_date = models.DateField()
    end_date = models.DateField()
    is_current = models.BooleanField(default=False)

    def __str__(self):
        return self.name


# =========================
# SEMESTER MODEL
# =========================
class Semester(models.Model):
    name = models.CharField(max_length=50)  # e.g., "Fall 2023", "Spring 2024"
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE)
    semester_number = models.IntegerField()  # 1, 2, 3, etc.
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.academic_year.name}"


# =========================
# HOD MODEL
# =========================
class HOD(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    department = models.OneToOneField(Department, on_delete=models.CASCADE, related_name="hod_user")
    phone = models.CharField(max_length=15)
    office_location = models.CharField(max_length=100, blank=True, null=True)
    joining_date = models.DateField()

    def __str__(self):
        return f"HOD of {self.department.name}"


# =========================
# ATTENDANCE MODEL
# =========================
class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(
        max_length=10,
        choices=[('Present', 'Present'), ('Absent', 'Absent'), ('Late', 'Late')],
        default='Present'
    )
    marked_by = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.fullname} - {self.course.coursename} - {self.date}"


# =========================
# PAYMENT MODEL
# =========================
class Payment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(
        max_length=20,
        choices=[
            ('Tuition Fee', 'Tuition Fee'),
            ('Library Fee', 'Library Fee'),
            ('Lab Fee', 'Lab Fee'),
            ('Exam Fee', 'Exam Fee'),
            ('Other', 'Other')
        ]
    )
    payment_date = models.DateField(auto_now_add=True)
    payment_method = models.CharField(
        max_length=20,
        choices=[
            ('Cash', 'Cash'),
            ('Card', 'Card'),
            ('Bank Transfer', 'Bank Transfer'),
            ('Online', 'Online')
        ]
    )
    status = models.CharField(
        max_length=10,
        choices=[('Paid', 'Paid'), ('Pending', 'Pending'), ('Failed', 'Failed')],
        default='Pending'
    )
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student.fullname} - {self.amount} - {self.status}"


# =========================
# STUDENT RESULT MODEL
# =========================
class StudentResult(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    internal_marks = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    external_marks = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_marks = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    grade = models.CharField(max_length=2, blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=[('Pass', 'Pass'), ('Fail', 'Fail'), ('Pending', 'Pending')],
        default='Pending'
    )

    def save(self, *args, **kwargs):
        self.total_marks = self.internal_marks + self.external_marks
        # Auto-calculate grade based on total marks
        if self.total_marks >= 90:
            self.grade = 'A+'
        elif self.total_marks >= 80:
            self.grade = 'A'
        elif self.total_marks >= 70:
            self.grade = 'B+'
        elif self.total_marks >= 60:
            self.grade = 'B'
        elif self.total_marks >= 50:
            self.grade = 'C'
        elif self.total_marks >= 40:
            self.grade = 'D'
        else:
            self.grade = 'F'
        
        # Auto-determine pass/fail
        self.status = 'Pass' if self.total_marks >= 40 else 'Fail'
        
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.fullname} - {self.course.coursename} - {self.grade}"