from django.db import models
from django.conf import settings


from django.contrib.auth import get_user_model

User = get_user_model()


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class ActiveStudentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_active=True)


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=20, unique=True)
    department = models.CharField(max_length=50)
    year_of_admission = models.IntegerField()
    profile_image = models.ImageField(
        upload_to="profile_images/", blank=True, null=True
    )
    courses = models.ManyToManyField(Course, blank=True)
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active = ActiveStudentManager()

    def __str__(self):
        return f"{self.user.username} - {self.roll_number }"


class Enrollment(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    grade = models.CharField(max_length=2, blank=True)
    date_enrolled = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "course")
