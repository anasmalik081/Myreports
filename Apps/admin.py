from django.contrib import admin
from .models import user_additional_detail, Report, Question, Answer

# Register your models here.
@admin.register(user_additional_detail)
class UserAdditionalDetails(admin.ModelAdmin):
    list_dispaly = ['user_id', 'address', 'mobile_number', 'phone_number', 'profile_image', 'is_doctor', 'is_patient', 'is_lab']

@admin.register(Report)
class UploadReports(admin.ModelAdmin):
    list_display = ['id', 'user' ,'report_id', 'report_name', 'lab_name','reffered_by' ,'patient_name', 'patient_mobile_number', 'lab_mobile_number', 'report_file_name', 'report_upload', 'report_img_name', 'report_image']


@admin.register(Question)
class UserQuestions(admin.ModelAdmin):
    list_display = ['id', 'user', 'first_name', 'last_name', 'question']

@admin.register(Answer)
class QueryAnswers(admin.ModelAdmin):
    list_display = ['id', 'question', 'answer']