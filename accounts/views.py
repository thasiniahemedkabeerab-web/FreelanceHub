from django.shortcuts import render, redirect
from .forms import SignupForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.shortcuts import render
from .models import FreelancerProfile
from .models import Job
from .forms import JobForm
from django.shortcuts import get_object_or_404
from .forms import JobApplicationForm
from .models import JobApplication
from .forms import FreelancerProfileForm
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import CustomUser, Job, JobApplication, FreelancerProfile
# def signup(request):
#     if request.method == "POST":
#         form = SignupForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('login')
#     else:
#         form = SignupForm()
#     return render(request, 'registration/signup.html', {'form': form})
def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)

        if form.is_valid():
            user = form.save()

            print("USER CREATED:", user.username)
            print("USER ID:", user.id)

            return redirect("login")

        else:
            print(form.errors)

    else:
        form = SignupForm()

    return render(request, "registration/signup.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.role == "admin":
                return redirect("admin_dashboard")
            elif user.role == "client":
                return redirect("client_dashboard")
            elif user.role == "freelancer":
                return redirect("freelancer_dashboard")

    return render(request, "registration/login.html")


def home(request):
    freelancers = FreelancerProfile.objects.all()

    context = {
        "freelancers": freelancers
    }

    return render(request, "home.html", context)

def job_list(request):
    jobs = Job.objects.all().order_by('-created_at')

    return render(request, 'dashboard/freelancer/jobs.html', {
        'jobs': jobs
    })


@login_required
def admin_dashboard(request):

    context = {
        "total_users": CustomUser.objects.count(),
        "total_freelancers": CustomUser.objects.filter(role="freelancer").count(),
        "total_clients": CustomUser.objects.filter(role="client").count(),
        "total_jobs": Job.objects.count(),
        "total_applications": JobApplication.objects.count(),
    }

    return render(
        request,
        "dashboard/admin_dashboard.html",
        context
    )
# @login_required
# def client_dashboard(request):
#     return render(request, 'dashboard/client_dashboard.html')

@login_required
def freelancer_dashboard(request):
    applications = JobApplication.objects.filter(freelancer=request.user)

    context = {
        "total_applications": applications.count(),
        "accepted_applications": applications.filter(status="Accepted").count(),
        "available_jobs": Job.objects.count(),
    }

    return render(request, 'dashboard/freelancer/freelancer_dashboard.html', context)
@login_required
def post_job(request):
    if request.user.role != "client":
        return redirect("home")

    if request.method == "POST":
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.client = request.user
            job.save()
            return redirect("job_list")
    else:
        form = JobForm()

    return render(
    request,
    "dashboard/client/post_job.html",
    {
        "form": form
    }
)
@login_required
def edit_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, client=request.user)

    if request.method == "POST":
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            return redirect('job_list')
    else:
        form = JobForm(instance=job)

    return render(request, 'post_job.html', {'form': form})


@login_required
def delete_job(request, job_id):
    job = get_object_or_404(Job, id=job_id, client=request.user)

    if request.method == "POST":
        job.delete()
        return redirect('job_list')

    return render(request, 'delete_job.html', {'job': job})
@login_required
def apply_job(request, job_id):

    if request.user.role != "freelancer":
        return redirect("home")

    job = get_object_or_404(Job, id=job_id)
    print(
    "Existing applications:",
    JobApplication.objects.filter(
        job=job,
        freelancer=request.user
    ).count()
)
    # Prevent duplicate applications
    if JobApplication.objects.filter(
        job=job,
        freelancer=request.user
    ).exists():

        messages.error(
            request,
            "You have already applied for this job."
        )

        return redirect("job_list")

    if request.method == "POST":

        form = JobApplicationForm(request.POST)

        if form.is_valid():

            application = form.save(commit=False)
            application.job = job
            application.freelancer = request.user
            application.save()

            messages.success(
                request,
                "Application submitted successfully."
            )

            return redirect("job_list")

    else:
        form = JobApplicationForm()

    return render(request, "apply_job.html", {
        "form": form,
        "job": job
    })
@login_required
def view_applications(request, job_id):

    if request.user.role != "client":
        return redirect("home")

    job = get_object_or_404(
        Job,
        id=job_id,
        client=request.user
    )

    applications = JobApplication.objects.filter(job=job)

    return render(
        request,
        "dashboard/client/view_applications.html",
        {
            "job": job,
            "applications": applications,
        }
    )
@login_required
def accept_application(request, application_id):
    application = get_object_or_404(
        JobApplication,
        id=application_id,
        job__client=request.user
    )

    application.status = "Accepted"
    application.save()

    return redirect('view_applications', job_id=application.job.id)


@login_required
def reject_application(request, application_id):
    application = get_object_or_404(
        JobApplication,
        id=application_id,
        job__client=request.user
    )

    application.status = "Rejected"
    application.save()

    return redirect('view_applications', job_id=application.job.id)
@login_required
def my_applications(request):

    applications = JobApplication.objects.filter(
        freelancer=request.user
    ).order_by("-applied_at")

    return render(
        request,
        "dashboard/freelancer/my_applications.html",
        {
            "applications": applications
        }
    )
@login_required
def edit_profile(request):

    if request.user.role != "freelancer":
        return redirect("home")

    profile, created = FreelancerProfile.objects.get_or_create(
       user=request.user,
    defaults={
        "title": "",
        "bio": "",
        "skills": "",
        "hourly_rate": 0,
        "experience": 0,
        "location": "",
    }
)

    if request.method == "POST":
        form = FreelancerProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect("freelancer_dashboard")

    else:
        form = FreelancerProfileForm(instance=profile)

    return render(request, "dashboard/freelancer/edit_profile.html", {
        "form": form
    })

def logout_view(request):
    logout(request)
    return redirect('login')
def about(request):
    return render(request, "about.html")


def contact(request):
    return render(request, "contact.html")
@login_required
def client_dashboard(request):
    jobs = Job.objects.filter(client=request.user)
    applications = JobApplication.objects.filter(job__client=request.user)

    context = {
        "total_jobs": jobs.count(),
        "total_applications": applications.count(),
        "pending_applications": applications.filter(status="Pending").count(),
    }

    return render(request, "dashboard/client_dashboard.html", context)

@login_required
def my_jobs(request):

    if request.user.role != "client":
        return redirect("home")

    jobs = Job.objects.filter(client=request.user).order_by("-created_at")

    return render(
        request,
        "dashboard/client/my_jobs.html",
        {
            "jobs": jobs
        }
    )
