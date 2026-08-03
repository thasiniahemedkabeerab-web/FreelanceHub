
# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('client', 'Client'),
        ('freelancer', 'Freelancer'),
    )

    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return self.username





class FreelancerProfile(models.Model):

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    profile_image = models.ImageField(
        upload_to='profiles/',
        blank=True,
        null=True
    )

    title = models.CharField(max_length=100)

    bio = models.TextField()

    skills = models.CharField(
        max_length=300,
        help_text="Example: Python, Django, React"
    )

    hourly_rate = models.DecimalField(
        max_digits=8,
        decimal_places=2
    )

    experience = models.PositiveIntegerField(
        help_text="Years of experience"
    )

    location = models.CharField(
        max_length=100
    )

    def __str__(self):
        return self.user.username

class Job(models.Model):

    client = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'client'}
    )

    title = models.CharField(max_length=200)

    category = models.CharField(max_length=100)

    description = models.TextField()

    budget = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    deadline = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
class JobApplication(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
    ]

    job = models.ForeignKey(
        Job,
        on_delete=models.CASCADE,
        related_name='applications'
    )

    freelancer = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'freelancer'}
    )

    proposal = models.TextField()

    bid_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    applied_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )

    def __str__(self):
        return f"{self.freelancer.username} - {self.job.title}"

    