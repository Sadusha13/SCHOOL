from django.db import models
from django.utils.text import slugify


class Teacher(models.Model):
	SUBJECT_CHOICES = [
		('Mathematics', 'Mathematics'),
		('English', 'English'),
		('Science', 'Science'),
		('History', 'History'),
		('Geography', 'Geography'),
		('Computer Science', 'Computer Science'),
		('Physical Education', 'Physical Education'),
		('Arts', 'Arts'),
		('Others', 'Others'),
	]

	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	employee_id = models.CharField(max_length=20, unique=True)
	gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')])
	date_of_birth = models.DateField()
	subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
	email = models.EmailField(unique=True)
	mobile_number = models.CharField(max_length=15)
	joining_date = models.DateField()
	teacher_image = models.ImageField(upload_to='teachers/', blank=True, null=True)
	qualification = models.CharField(max_length=100, blank=True)
	experience = models.IntegerField(default=0, help_text="Years of experience")
	address = models.TextField(blank=True)
	slug = models.SlugField(max_length=255, unique=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def save(self, *args, **kwargs):
		if not self.slug:
			base_slug = slugify(f"{self.first_name}-{self.last_name}-{self.employee_id}")
			slug = base_slug
			counter = 1
			while Teacher.objects.filter(slug=slug).exclude(pk=self.pk).exists():
				slug = f"{base_slug}-{counter}"
				counter += 1
			self.slug = slug
		super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.first_name} {self.last_name} ({self.employee_id})"

	class Meta:
		ordering = ['-created_at']

# Create your models here.
