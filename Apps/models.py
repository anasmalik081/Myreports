from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from .fileValidator import FileValidator



class user_additional_detail(models.Model):
    user_id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    address = models.TextField(max_length=500)
    mobile_number = PhoneNumberField(blank=True, null=True)
    phone_number = PhoneNumberField(blank=True, help_text='Replace Initial 0 with Country Code')
    profile_image = models.ImageField(blank=True, null=True ,upload_to='profileimg', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])])
    clinic_name = models.CharField(max_length=100, blank=True, null=True)
    lab_name = models.CharField(max_length=100, blank=True, null=True)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_lab = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    # updated_by=models.ForeignKey(User,on_delete=models.CASCADE ,related_name='updated_by_user')
    # created_by=models.ForeignKey(User,on_delete=models.CASCADE, related_name='created_by_user')

    def __str__(self):
        if self.is_doctor == True:
            return User.get_username(self.user_id) + " - is_doctor"

        elif self.is_lab == True:
            return User.get_username(self.user_id) + "-is_lab"

        elif self.is_patient == True:
            return User.get_username(self.user_id) + " - is_patient"
            
        else:
            return User.get_username(self.user_id) + "-is_not decided Yet"
            
    
class Report(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_reports")
    report_id = models.CharField(max_length=100)
    report_name = models.CharField(max_length=100)
    reffered_by = models.CharField(max_length=100, blank=True, null=True)
    lab_name = models.CharField(max_length=50)
    patient_name = models.CharField(max_length=50)
    patient_mobile_number = PhoneNumberField()
    lab_mobile_number = PhoneNumberField(blank=True)
    report_file_name = models.CharField(max_length=50)
    report_upload = models.FileField(upload_to='reports',validators=[FileValidator(max_size=(2*1024*1024) , allowed_extensions=('pdf', 'doc', 'docx'))])
    report_img_name = models.CharField(max_length=100, null=True)
    report_image = models.ImageField(blank=True, null=True ,upload_to='reports/img', validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])])
    create_date = models.DateTimeField(auto_now_add=False, auto_now=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['report_id', 'lab_name'], name='unique_report_lab_report_id'),
        ]
    
class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    question = models.TextField(max_length=500)

class Answer(models.Model):
    question = models.TextField(max_length=500)
    answer = models.TextField(max_length=2000)