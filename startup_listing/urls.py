from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('community/<int:id>', views.community, name="community"),
    path('project/<int:id>', views.project, name="project"),
    path('profile/<str:username>', views.profile, name="profile"),
    path('startup_listing', views.startup_listing, name='startup_listing'),
    path('startup_home/<int:id>', views.startup_home, name="startup_home"),
    path('profile_edit/<str:username>', views.profile_edit, name="profile_edit"),
    path('add_project', views.add_project, name="add_project"),
    path('project_details_startup/<int:pk>', views.project_details_startup, name="project_details_startup"),
    path('add_skills/', views.add_skills, name="add_skills"),
    path('add_tags', views.add_tags, name="add_tags"),
    path('add_form_field/<int:id>', views.add_form_field, name="add_form_field"),
    path('delete_field/<int:pk>', views.delete_field, name="delete_field"),
    path('approval/', views.approval, name="approval"),
    path('registration/', views.registration, name="registration"),
]