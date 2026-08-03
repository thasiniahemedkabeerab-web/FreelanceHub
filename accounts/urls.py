from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('', views.home, name='home'),
    path('jobs/', views.job_list, name='job_list'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('client-dashboard/', views.client_dashboard, name='client_dashboard'),
    path('freelancer-dashboard/', views.freelancer_dashboard, name='freelancer_dashboard'),
    path('post-job/', views.post_job, name='post_job'),
    path('edit-job/<int:job_id>/', views.edit_job, name='edit_job'),
    path('delete-job/<int:job_id>/', views.delete_job, name='delete_job'),
    path('apply-job/<int:job_id>/', views.apply_job, name='apply_job'),
    path('accept-application/<int:application_id>/',views.accept_application,name='accept_application'),
path('reject-application/<int:application_id>/',views.reject_application,name='reject_application'),
path(
    'my-applications/',
    views.my_applications,
    name='my_applications'
),
path(
    'edit-profile/',
    views.edit_profile,
    name='edit_profile'
),
path(
    "my-jobs/",
    views.my_jobs,
    name="my_jobs"
),
path(
    "job/<int:job_id>/applications/",
    views.view_applications,
    name="view_applications",
),

path(
    "application/<int:application_id>/accept/",
    views.accept_application,
    name="accept_application",
),

path(
    "application/<int:application_id>/reject/",
    views.reject_application,
    name="reject_application",
),

path('logout/', views.logout_view, name='logout'),
path('about/', views.about, name='about'),
path('contact/', views.contact, name='contact'),
]

