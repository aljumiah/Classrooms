from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegister, UserLogin, AddStudent
from .models import Classroom, Students
from .forms import ClassroomForm
from django.contrib.auth import login, authenticate, logout

def classroom_list(request):
	classrooms = Classroom.objects.all()
	context = {
		"classrooms": classrooms,
	}
	return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):
	if request.user.is_anonymous:
		return redirect('login')
	classroom = Classroom.objects.get(id=classroom_id)
	students = Students.objects.filter(classroom=classroom).order_by('name','-exam_grade')

	context = {
		"classroom": classroom,
		"students": students
	}
	return render(request, 'classroom_detail.html', context)


def classroom_create(request):
	if request.user.is_anonymous:
		return redirect('login')
	form = ClassroomForm()
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None)
		if form.is_valid():
			
			classroom = form.save(commit=False)
			classroom.teacher = request.user
			classroom.save()

			messages.success(request, "Successfully Created!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	}
	return render(request, 'create_classroom.html', context)


def classroom_update(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)

	if request.user.is_anonymous:
		return redirect('login')
	elif not (request.user.is_staff or request.user == classroom.teacher):
		return redirect('no-access')

		
	classroom = Classroom.objects.get(id=classroom_id)
	form = ClassroomForm(instance=classroom)
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None, instance=classroom)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	"classroom": classroom,
	}
	return render(request, 'update_classroom.html', context)


def classroom_delete(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)

	if request.user.is_anonymous:
		return redirect('login')
	elif not (request.user.is_staff or request.user == classroom.teacher):
		return redirect('no-access')

	Classroom.objects.get(id=classroom_id).delete()
	messages.success(request, "Successfully Deleted!")
	return redirect('classroom-list')


def user_register(request):
        form = UserRegister()
        if request.method == 'POST':
            form = UserRegister(request.POST)
            if form.is_valid():
                user = form.save(commit=False)
                 # the encryption for the password goes here
                user.set_password(user.password)
                user.save()    
                login(request, user)
                # Where you want to go after a successful signup
                return redirect("classroom-list")  
        context = {
            "form":form,
        }
        return render(request, 'register.html', context)


def user_login(request):
        form = UserLogin()
        if request.method == 'POST':
            form = UserLogin(request.POST)
            if form.is_valid():

                username = form.cleaned_data['username']
                password = form.cleaned_data['password']

                auth_user = authenticate(username=username, password=password)
                if auth_user is not None:
                    login(request, auth_user)
                    # Where you want to go after a successful login
                    return redirect('classroom-list')

        context = {
            "form":form
        }
        return render(request, 'login.html', context)

def logout_view(request):
            logout(request)
            return redirect('login')


def no_access(request):
    return render(request, 'no_access.html')


def add_student(request, classroom_id):
    form = AddStudent()
    classroom = Classroom.objects.get(id=classroom_id)
	
    if not (request.user.is_staff or request.user == classroom.teacher):
        return redirect('no-access')

    if request.method == "POST":
        form = AddStudent(request.POST)
        if form.is_valid():
            student = form.save(commit=False)
            student.classroom = classroom
            student.save()
            return redirect('classroom-detail', classroom_id)
    context = {
        "form":form,
        "classroom": classroom,
    } 
    return render(request, 'student_create.html', context )



def student_update(request,classroom_id, student_id):
	student = Students.objects.get(id=student_id)
	classroom = Classroom.objects.get(id=classroom_id)
	classroom = Classroom.objects.get(id=classroom_id)

	if not (request.user.is_staff or request.user == classroom.teacher):
		return redirect('no-access')

	form = AddStudent(instance=student)
	if request.method == "POST":
		form = AddStudent(request.POST, instance=student)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
			return redirect('classroom-detail',classroom_id)
		print (form.errors)
	context = {
	"form": form,
	"student": student,
	"classroom": classroom

	}
	return render(request, 'student_update.html', context)


def student_delete(request, student_id,classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)

	if not (request.user.is_staff or request.user == classroom.teacher):
		return redirect('no-access')
	Students.objects.get(id=student_id).delete()
	messages.success(request, "Successfully Deleted!")
	return redirect('classroom-detail' , classroom_id)
