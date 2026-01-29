from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Teacher
from school.models import Notification


def create_notification(user, message):
	Notification.objects.create(user=user, message=message)


@login_required
def teacher_list(request):
	teachers = Teacher.objects.all()
	return render(request, 'teachers/teachers.html', {'teachers': teachers})


@login_required
def add_teacher(request):
	if request.method == 'POST':
		data = request.POST
		teacher_image = request.FILES.get('teacher_image')

		teacher = Teacher(
			first_name=data.get('first_name'),
			last_name=data.get('last_name'),
			employee_id=data.get('employee_id'),
			gender=data.get('gender'),
			date_of_birth=data.get('date_of_birth'),
			subject=data.get('subject'),
			email=data.get('email'),
			mobile_number=data.get('mobile_number'),
			joining_date=data.get('joining_date'),
			qualification=data.get('qualification') or '',
			experience=data.get('experience') or 0,
			address=data.get('address') or '',
			teacher_image=teacher_image
		)
		teacher.save()
		create_notification(request.user, f"Added teacher: {teacher.first_name} {teacher.last_name}")
		messages.success(request, "Teacher added successfully")
		return redirect('teachers:view_teacher', slug=teacher.slug)

	return render(request, 'teachers/add-teacher.html', {
		'subjects': Teacher._meta.get_field('subject').choices
	})


@login_required
def view_teacher(request, slug):
	teacher = get_object_or_404(Teacher, slug=slug)
	return render(request, 'teachers/teacher-details.html', {'teacher': teacher})


@login_required
def edit_teacher(request, slug):
	teacher = get_object_or_404(Teacher, slug=slug)

	if request.method == 'POST':
		data = request.POST
		teacher.first_name = data.get('first_name')
		teacher.last_name = data.get('last_name')
		teacher.gender = data.get('gender')
		teacher.date_of_birth = data.get('date_of_birth')
		teacher.subject = data.get('subject')
		teacher.email = data.get('email')
		teacher.mobile_number = data.get('mobile_number')
		teacher.joining_date = data.get('joining_date')
		teacher.qualification = data.get('qualification') or ''
		teacher.experience = data.get('experience') or 0
		teacher.address = data.get('address') or ''
		if request.FILES.get('teacher_image'):
			teacher.teacher_image = request.FILES.get('teacher_image')
		teacher.save()
		messages.success(request, "Teacher updated successfully")
		return redirect('teachers:view_teacher', slug=teacher.slug)

	return render(request, 'teachers/edit-teacher.html', {
		'teacher': teacher,
		'subjects': Teacher._meta.get_field('subject').choices
	})


@login_required
def delete_teacher(request, slug):
	teacher = get_object_or_404(Teacher, slug=slug)
	if request.method == 'POST':
		teacher.delete()
		messages.success(request, "Teacher deleted successfully")
		return redirect('teachers:teacher_list')
	return render(request, 'teachers/delete-teacher.html', {'teacher': teacher})

# Create your views here.
