from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404, reverse
from .models import Student, Librarian, Materials, Forum, Comments
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.contrib.auth import authenticate, login
from django.utils import timezone
from datetime import date
# Create your views here.


def homepage(request):
    return render(request, 'index.html')

def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        info = auth.authenticate(username=email, password=password)
        if info is not None:
            login(request, info)
            if info.is_superuser:
                return redirect('librarian_dashboard')
            elif info.is_staff:
                return redirect('student_dashboard')
            else:
                messages.error(request, "Wait for Admin Confirmation to your Account.")
                return redirect('login')
        else:
            messages.error(request, "Invalid email or password")
            return redirect('login')
    return render(request, 'login.html')

def logoutUser(request):
    auth.logout(request)
    messages.success(request, "Logged out Successfully!")
    return redirect('login')








def student_signup(request):
    if request.method == 'POST':
        full_name = request.POST['fullname']
        email = request.POST['email']
        year = request.POST['year']
        course = request.POST['course']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Email already taken.')
                return redirect('student_signup')

            else:
                new_student = User.objects.create_user(
                    first_name=full_name, email=email, password=password1, is_staff=False, is_superuser=False, username=email )
                new_student.save()

                profile_currentStud = Student.objects.create(
                    user=new_student, course=course, year=year)
                profile_currentStud.save()
                messages.success(request, 'Account created')
                return redirect('login')
        else:
            messages.error(request, 'Password does not match.')
            return redirect('student_signup')
    return render(request, 'signup.html')

@login_required(login_url='/login')
def student_dashboard(request):
    number_of_materials = Materials.objects.count()
    today = timezone.now().date()  # Current date
    
    authenticated_user = request.user
    borrowed = Materials.objects.filter(borrower=authenticated_user.first_name)
    
    for item in borrowed:
        if item.deadline.date() < today:
            item.overdue = True
            item.remaining_days = None  # No need to calculate remaining days if overdue
        else:
            item.overdue = False
            item.remaining_days = (item.deadline.date() - today).days
    
    context = {
        'borrowed': borrowed, 
        'today': today,
        'number_of_materials': number_of_materials,
    }
    return render(request, 'student/dashboard.html', context)

@login_required(login_url='/login')
def student_materials(request):
    current_date = date.today()
    materials = Materials.objects.all().order_by('-id')
    number_of_materials = Materials.objects.count()
    authenticated_user = request.user 
    
    if request.method == 'POST':
        material_id = request.POST.get('material_id')
        material = Materials.objects.get(pk=material_id)
        
        # Update the material fields based on form data
        material.borrowed_date = request.POST.get('start')
        material.deadline = request.POST.get('end')
        material.borrower = authenticated_user.first_name
        material.status = 'Not Available'
        
        # Get the associated Student instance
        student_instance = Student.objects.get(user=authenticated_user)
        
        # Assign the borrower year, course from the Student instance
        material.borrower_year = student_instance.year
        material.borrower_course = student_instance.course
        
        # Save the updated material
        material.save()
        messages.success(request, 'Materials Borrowed')
        
    context = {
        'materials': materials,
        'number_of_materials': number_of_materials,
        'current_date': current_date,
    }
    return render(request, 'student/materials.html', context)


@login_required(login_url='/login')
def student_forum(request):
   
    forums = Forum.objects.all().annotate(comment_count=Count('comments')).order_by('-upload_date')
    comments_lists = Comments.objects.all().order_by('comment_date')

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        file = request.FILES.get('file')  # Use get() to avoid KeyError
        
        # Get the current user
        uploader = request.user

        # Create the forum with the current user as uploader
        new_forum = Forum.objects.create(title=title, description=description, uploader=uploader, file=file)
        new_forum.save()
        messages.success(request, 'Forum Added!')

             
       
    number_of_materials = Materials.objects.count()
    context = {
        'forums': forums,
        'comments_lists': comments_lists,
        'number_of_materials':number_of_materials,
    }
    return render(request, 'student/forums.html', context)


@login_required(login_url='/login')
def forum_page(request):
   
    authenticated_user = request.user
    
    # Retrieve the corresponding student object
    student = get_object_or_404(Student, user=authenticated_user)
    
    # Retrieve all forums with comment counts
    forums = Forum.objects.annotate(comment_count=Count('comments')).order_by('-upload_date')
    
    if request.method == 'POST':
        comment = request.POST['comment']
        commentor = request.POST['commentor']
        post_id = request.POST['post']  # Retrieve the post ID
        
        # Get the corresponding Forum instance
        forum = get_object_or_404(Forum, pk=post_id)
        
        new_comment = Comments.objects.create(comment=comment, commentors=student.user, post=forum)
        new_comment.save()
    
    # Get the forum_id from the query parameters
    forum_id = request.GET.get('forum_id')

    # Retrieve the forum object using the forum_id
    forum = Forum.objects.get(id=forum_id)

    # Retrieve all comments related to the forum
    comments = Comments.objects.filter(post=forum)
    
    
    number_of_materials = Materials.objects.count()
    context = {
        'forum': forum, 
        'comments': comments,
        'student':student,
        'number_of_materials':number_of_materials,
    }
    # Render the forum page template with the forum object and comments
    return render(request, 'student/forumPost.html', context)











def librarian_signup(request):
    if request.method == 'POST':
        full_name = request.POST['fullname']
        email = request.POST['email']
        role = request.POST['role']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        if password1 == password2:
            if User.objects.filter(username=email).exists():
                messages.error(request, 'Email already taken.')
                return redirect('librarian_signup')

            else:
                new_librarian = User.objects.create_user(
                    first_name=full_name, email=email, password=password1, is_staff=False, is_superuser=False, username=email )
                new_librarian.save()

                profile_currentStud = Librarian.objects.create(
                    user=new_librarian, role=role)
                profile_currentStud.save()
                messages.success(request, 'Account created')
                return redirect('login')
        else:
            messages.error(request, 'Password does not match.')
            return redirect('librarian_signup')
    return render(request, 'signup1.html')


@login_required(login_url='/login')
def librarian_dashboard(request):
    materials = Materials.objects.filter(status='Not Available')
    
    context = {
        'materials': materials,
    }
    return render(request, 'librarian/dashboard.html', context)


@login_required(login_url='/login')
def materials(request):
    materials = Materials.objects.all().order_by('-id')
    
    if request.method == 'POST':
        material_name = request.POST.get('material_name')
        uploaded_file = request.FILES.get('file')

        new_material = Materials.objects.create(name=material_name, profile_pic=uploaded_file, status='Available' )
        new_material.save()
        messages.success(request, 'Materials Added')
        
    context = {
        'materials': materials,
    }
    return render(request, 'librarian/materials.html', context)


def update_material(request, material_id):
    # Assuming you have a Material model
    material = Materials.objects.get(id=material_id)
    
    # Update the material data (for demonstration, setting all fields to blank)

    material.borrower = ''
    material.status = 'Available'
    material.borrower_year = ''
    material.borrower_course = ''
    material.borrowed_date = None
    material.deadline = None
    
    # Save the changes
    material.save()
    
    # Redirect back to the same page
    messages.success(request, 'Material will be Available again.')
    return redirect('/librarian_dashboard')

def delete_material(request, material_id):
    Materials.objects.filter(id=material_id).delete()
    messages.success(request, 'Material deleted')
    return redirect('/materials')



@login_required(login_url='/login')
def librarian_forum(request):
   
    forums = Forum.objects.all().annotate(comment_count=Count('comments')).order_by('-upload_date')
    comments_lists = Comments.objects.all().order_by('comment_date')

    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        file = request.FILES.get('file')  # Use get() to avoid KeyError
        
        # Get the current user
        uploader = request.user

        # Create the forum with the current user as uploader
        new_forum = Forum.objects.create(title=title, description=description, uploader=uploader, file=file)
        new_forum.save()
        messages.success(request, 'Forum Added!')

             
       
    number_of_materials = Materials.objects.count()
    context = {
        'forums': forums,
        'comments_lists': comments_lists,
        'number_of_materials':number_of_materials,
    }
    return render(request, 'librarian/forums.html', context)


@login_required(login_url='/login')
def forum_page1(request):
   
    authenticated_user = request.user
    
    # Retrieve the corresponding student object
    librarian = get_object_or_404(Librarian, user=authenticated_user)
    
    # Retrieve all forums with comment counts
    forums = Forum.objects.annotate(comment_count=Count('comments')).order_by('-upload_date')
    
    if request.method == 'POST':
        comment = request.POST['comment']
        post_id = request.POST['post']  # Retrieve the post ID
        
        # Get the corresponding Forum instance
        forum = get_object_or_404(Forum, pk=post_id)
        
        new_comment = Comments.objects.create(comment=comment, commentors=librarian.user, post=forum)
        new_comment.save()
    
    # Get the forum_id from the query parameters
    forum_id = request.GET.get('forum_id')

    # Retrieve the forum object using the forum_id
    forum = Forum.objects.get(id=forum_id)

    # Retrieve all comments related to the forum
    comments = Comments.objects.filter(post=forum)
    
    
    number_of_materials = Materials.objects.count()
    context = {
        'forum': forum, 
        'comments': comments,
        'librarian':librarian,
        'number_of_materials':number_of_materials,
    }
    # Render the forum page template with the forum object and comments
    return render(request, 'librarian/forumPost.html', context)






def main_login(request):
    return render(request, 'main/mainLogin.html')

def main_students(request):
    student = Student.objects.all().order_by('-id')
    
    context = {
        'student': student,
    }
    return render(request, 'main/students.html', context)

def main_librarian(request):
    librarian = Librarian.objects.all().order_by('-id')
    
    context = {
        'librarian': librarian,
    }
    return render(request, 'main/librarians.html', context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')






def approve_student(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_staff = True
    user.save()
    messages.success(request, 'Student set to Approved')
    # You can redirect to a success page or to the same page
    return redirect('main_students')

def deleteStudent1(request, student_id):
    Student.objects.filter(id=student_id).delete()
    messages.success(request, 'Student Removed')
    return redirect('/main_students')

def deleteLibrarian1(request, librarian_id):
    Librarian.objects.filter(id=librarian_id).delete()
    messages.success(request, 'Librarian Removed')
    return redirect('/main_librarian')

def deleteLStudent1(request, student_id):
    Student.objects.filter(id=student_id).delete()
    messages.success(request, 'Student Removed')
    return redirect('/main_students')

def disapprove_student(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_staff = False
    user.save()
    messages.success(request, 'Student set to Not Approve')
    # You can redirect to a success page or to the same page
    return redirect('main_students')


def approve_librarian(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_superuser = True
    user.save()
    messages.success(request, 'Librarian set to Approve')
    # You can redirect to a success page or to the same page
    return redirect('main_librarian')

def disapprove_librarian(request, user_id):
    user = User.objects.get(pk=user_id)
    user.is_superuser = False
    user.save()
    messages.success(request, 'Librarian set to Not Approve')
    # You can redirect to a success page or to the same page
    return redirect('main_librarian')



def collection(request):
    materials = Materials.objects.all().order_by('-id')
    
    context = {
        'materials': materials
    }
    return render(request, 'collection.html', context)