from django.urls import path
from . import views


urlpatterns = [
    
    path('deletelibrarian1/<int:librarian_id>/', views.deleteLibrarian1, name='deletelibrarian1'),
    path('approve-librarian/<int:user_id>/', views.approve_librarian, name='approve_librarian'),
    path('disapprove-librarian/<int:user_id>/', views.disapprove_librarian, name='disapprove_librarian'),
    
    path('approve-student/<int:user_id>/', views.approve_student, name='approve_student'),
    path('disapprove-student/<int:user_id>/', views.disapprove_student, name='disapprove_student'),
    path('deletestudent1/<int:student_id>/', views.deleteStudent1, name='deletestudent1'),
    
    
    path('main_login', views.main_login, name='main_login'),
    path('main_students', views.main_students, name='main_students'),
    path('main_librarian', views.main_librarian, name='main_librarian'),
    
    
    path('collection', views.collection, name='collection'),
    path('about', views.about, name='about'),
    path('contact', views.contact, name='contact'),
    path('homepage', views.homepage, name='homepage'),
    path('login', views.user_login, name='login'),
    path('logout', views.logoutUser, name='logout'), 
    
    path('student_signup', views.student_signup, name='student_signup'),
    path('student_dashboard', views.student_dashboard, name='student_dashboard'),
    path('student_materials', views.student_materials, name='student_materials'),
    path('student_forum', views.student_forum, name='student_forum'),
    path('forum_page', views.forum_page, name='forum_page'),
    
    
    path('librarian_signup', views.librarian_signup, name='librarian_signup'),
    path('librarian_dashboard', views.librarian_dashboard, name='librarian_dashboard'),
    path('materials', views.materials, name='materials'),
    path('librarian_forum', views.librarian_forum, name='librarian_forum'),
    path('forum_page1', views.forum_page1, name='forum_page1'),
    
    
    path('update_material/<int:material_id>/', views.update_material, name='update_material'),
    path('<int:material_id>/deletematerial/', views.delete_material, name='deletematerial'),
]