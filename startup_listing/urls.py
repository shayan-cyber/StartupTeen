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
    path('add_benefits/', views.add_benefits, name="add_benefits"),
    path('add_tags', views.add_tags, name="add_tags"),
    path('add_form_field/<int:id>', views.add_form_field, name="add_form_field"),
    path('delete_field/<int:pk>', views.delete_field, name="delete_field"),
    path('approval/', views.approval, name="approval"),
    path('register/', views.register, name="register"),
    path('register_sign_up/', views.sign_up, name="register_sign_up"),
    path('login_page/', views.login_page, name="login_page"),
    path('add_startup/', views.add_startup, name="add_startup"),
    path('startup_dashboard/', views.startup_dashboard, name="startup_dashboard"),
    path('communities', views.communities, name="communities"),
    path('edit_startup/<int:pk>', views.edit_startup, name="edit_startup"),
    path('edit_project/<int:pk>', views.edit_project, name="edit_project"),
    path('delete_project/<int:pk>', views.delete_project, name="delete_project"),
    path('completed_project/<int:pk>', views.completed_project, name="completed_project"),
    path('tag_link/<int:pk>', views.tag_link, name="tag_link"),
    path('explore_section', views.explore_section, name="explore_section"),
    path('log_out', views.log_out, name="log_out")
]