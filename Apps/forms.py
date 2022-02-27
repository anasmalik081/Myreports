from datetime import datetime
import email
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from phonenumber_field.widgets import PhoneNumberPrefixWidget
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.utils.translation import gettext_lazy as _
from django.shortcuts import get_object_or_404
from django.contrib.auth import password_validation
from Apps.models import user_additional_detail, Report, Question
from phonenumber_field.modelfields import PhoneNumberField



USER_CHOICE = (
    ('','----------------'),
    ('doctor', 'Doctor'),
    ('patient', 'Patient'),
    ('lab', 'Lab'),
)
##########################
    # def clean_phone_number(self):
    #     phone_number = self.data.get('phone_number')
    #     print(phone_number)
    #     if User.objects.filter(phone_number=phone_number).exists():
    #         raise forms.ValidationError(
    #             _("Another user with this phone number already exists"))
    #     if len(phone_number) == 10 and phone_number.isdigit():
    #         pass
    #     else:
    #         raise forms.ValidationError(
    #             _("Invalid Phone Number"))
    #     return phone_number
############################################################
class CustomerRegistrationForm(UserCreationForm):
    required_css_class = 'required'
    user_type = forms.ChoiceField(required=True ,label="Select Your Category", choices=USER_CHOICE, widget=forms.Select(attrs={'class':'form-select'}))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class':'form-control'}))
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class':'form-control'}))
    lab_name = forms.CharField(required=False,label='Lab Name', widget=forms.TextInput(attrs={'class':'form-control', 'id':'lab_name'}))
    clinic_name = forms.CharField(required=False,label='Clinic Name', widget=forms.TextInput(attrs={'class':'form-control', 'id':'clinic_name'}))
    class Meta:
        model = User
        fields = ['user_type','lab_name', 'clinic_name' , 'username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class':'form-control'}),
        }
    
    def clean_clinic_name(self):
        try:
            data = self.cleaned_data["user_type"]
            if data == "doctor":
                if self.cleaned_data["clinic_name"]=='':
                    raise forms.ValidationError("Please Enter Your Clinic Name")

            return self.cleaned_data["clinic_name"]
        except(KeyError,ValueError):
            raise forms.ValidationError("This Field is Required")

    def clean_lab_name(self):
        try:
            data = self.cleaned_data["user_type"]
            if data == "lab":
                if self.cleaned_data["lab_name"]=='':
                    raise forms.ValidationError("Please Enter Your Lab Name")

            return self.cleaned_data["lab_name"]
        except(KeyError,ValueError):
            raise forms.ValidationError("This Field is Required")

    def clean_email(self):
        try:
            email = User.objects.get(email=self.cleaned_data['email'])
            raise forms.ValidationError("Email already exists.")
        except User.DoesNotExist:
            return self.cleaned_data['email']


    
    
class LoginForm(AuthenticationForm):
    required_css_class = 'required'
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True, 'class':'form-control'}))
    password = forms.CharField(label=_('Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username', 'password']


class AddProfileForm(forms.ModelForm):
    required_css_class = 'required'
    class Meta:
        model = user_additional_detail
        fields = ['address', 'mobile_number', 'phone_number', 'profile_image']
        widgets = {
            'address': forms.TextInput(attrs={'class':'form-control'}),
            'mobile_number': PhoneNumberPrefixWidget(initial='IN',attrs={'class':'form-control col me-2', 'placeholder':'Mobile Number'}),
            'phone_number': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}),
            'profile_image': forms.FileInput(attrs={'class':'form-control'}),
        }


class ReportUploadForm(forms.ModelForm):
    required_css_class = 'required'
    report_image = forms.ImageField(required=False,label='Any Report Image?', widget=forms.FileInput(attrs={'class':'form-control'}))
    report_id = forms.CharField(required=False, widget= forms.TextInput(attrs={'autocomplete': 'off','class':'form-control', 'placeholder':'Report ID or Autogenerated' }))
    class Meta:
        model = Report
        fields = ['report_id', 'report_name', 'lab_name', 'reffered_by', 'patient_name', 'patient_mobile_number', 'lab_mobile_number', 'report_upload', 'report_image']
        widgets = {
            'report_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Report Name'}),
            'reffered_by': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Reffered Doctor Name'}),
            'lab_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Lab Name'}),
            'patient_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Please Enter Full Name'}),
            'patient_mobile_number': PhoneNumberPrefixWidget(initial='IN' ,attrs={'class':'form-control col me-2', 'placeholder':'Patient Mobile Number'}),
            'lab_mobile_number': PhoneNumberPrefixWidget(initial='IN' ,attrs={'class':'form-control col me-2', 'placeholder':'Optional'}),
            'report_upload': forms.FileInput(attrs={'class':'form-control'}),
        }

    def clean_report_id(self):
        report_id = self.cleaned_data['report_id']
        for char in report_id:
            if not char.isdigit() and not char.isalpha():
                raise forms.ValidationError("Report Id can only be aplha-numeric")
        return report_id
    
    def clean_patient_name(self):
        patient_name = self.cleaned_data['patient_name']
        for char in patient_name:
            if char.isspace()== False and not char.isalpha():
                raise forms.ValidationError("Patient Name can only be aplhabetic")
        return patient_name

    def clean_report_name(self):
        report_name = self.cleaned_data['report_name']
        for char in report_name:
            if '.'==char:
                raise forms.ValidationError("report_name should not have '.' with name")
            if char.isspace()== False and not char.isalpha():
                raise forms.ValidationError("report_name can only be aplhabetic")
        return report_name


class QuestionsForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['question']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'})
        }


class PasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_('Old Password'), strip=False, widget=forms.PasswordInput(attrs={'autofocus': True, 'autocomplete': 'current-password', 'class': 'form-control'}))
    new_password1 = forms.CharField(label=_('New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_('Confirm Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'current-password', 'class': 'form-control'}))


class PasswordReset(PasswordResetForm):
    email = forms.CharField(required=True, label='Email', widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class':'form-control'}))
    error_messages = {
        'unknown': ("That email address doesn't have an associated "
                     "user account. Are you sure you've registered?"),
        'unusable': ("The user account associated with this email "
                      "address cannot reset the password."),
        }
    def clean_email(self):
        """
        Validates that an active user exists with the given email address.
        """
        UserModel = get_user_model()
        email = self.cleaned_data["email"]
        self.users_cache = UserModel._default_manager.filter(email__iexact=email)
        if not len(self.users_cache):
            raise forms.ValidationError(self.error_messages['unknown'])
        if not any(user.is_active for user in self.users_cache):
            # none of the filtered users are active
            raise forms.ValidationError(self.error_messages['unknown'])
        # if any((user.password == UNUSABLE_PASSWORD)
        #     for user in self.users_cache):
        #     raise forms.ValidationError(self.error_messages['unusable'])
        return email


class SetPassword(SetPasswordForm):
    new_password1 = forms.CharField(label=_('New Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control', 'id':'id_password'}), help_text=password_validation.password_validators_help_text_html())
    new_password2 = forms.CharField(label=_('Confirm Password'), strip=False, widget=forms.PasswordInput(attrs={'autocomplete': 'new password', 'class': 'form-control'}))
