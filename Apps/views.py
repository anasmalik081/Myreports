import datetime
from unicodedata import name
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from .forms import CustomerRegistrationForm, LoginForm, AddProfileForm, ReportUploadForm, QuestionsForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib import messages
from .filters import DoctorFilter, LabFilter
from .models import Answer, Question, Report, user_additional_detail
from django.contrib.auth.models import Group



# Create your views here.

groups = Group.objects.get_or_create(name = 'Doctor')
groups = Group.objects.get_or_create(name = 'Lab')
groups = Group.objects.get_or_create(name = 'Patient')

def home(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user)
        user_type = user_additional_detail.objects.get(user_id=user)
        if user_type.is_doctor:
            t_refferals = Report.objects.filter(Q(reffered_by__contains= request.user.first_name) & Q(reffered_by__contains= request.user.last_name))
            m_refferals = Report.objects.filter(Q(create_date__gte=f"{datetime.datetime.now().strftime('%Y-%m')}-01") & Q(reffered_by__contains=request.user.first_name))
            return render(request, 'home.html', {'total':t_refferals, 'month':m_refferals})
        else:
            return render(request, 'home.html')
    else:
        return render(request, 'home.html')

def contact(request):
    return render(request, 'contact.html')

@method_decorator(login_required, name='dispatch')
class ContactUs(View):
    def get(self, request):
        form = QuestionsForm()
        return render(request, 'contact_us.html', {'form':form})

    def post(self, request):
        form = QuestionsForm(request.POST)
        if form.is_valid():
            user = request.user
            first_name = request.user.first_name
            last_name = request.user.last_name
            question = form.cleaned_data['question']
            query = Question(user=user, first_name=first_name, last_name=last_name, question=question)
            query.save()
            messages.success(request, "Your question has been successfully added in our question list. We will answer you shortly")
        return render(request, 'contact_us.html', {'form':form})


User = get_user_model()
class CutomerRegistration(View):
    def get(self, request):
        form = CustomerRegistrationForm()
        return render(request, 'register.html', {'form':form})

    def post(self, request):
        form = CustomerRegistrationForm(request.POST)
        vendor_type = request.POST.get('user_type')

        if form.is_valid():
            
            user=form.save()

            user_type = None
            if vendor_type == 'doctor':
                user_type = user_additional_detail(user_id=user,is_doctor=True, clinic_name=request.POST.get('clinic_name'))
                group = Group.objects.get(name='Doctor')
                user.groups.add(group)
            elif vendor_type == 'patient':
                user_type = user_additional_detail(user_id=user,is_patient=True)
                group = Group.objects.get(name='Patient')
                user.groups.add(group)
            elif vendor_type == 'lab':
                user_type = user_additional_detail(user_id=user,is_lab=True, lab_name=request.POST.get('lab_name'))
                group = Group.objects.get(name='Lab')
                user.groups.add(group)
            
            user_type.save()
            messages.success(request, 'Congratulations! You are Registered Successfully.')
            return redirect('login')
        return render(request, 'register.html', {'form':form})

class UserLogin(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'login.html', {'form':form})

    def post(self, request):
        form = LoginForm(request,request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']         
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                vendor_type = user_additional_detail.objects.get(user_id=user)
                if user.is_authenticated and vendor_type.is_doctor:
                    return redirect('home')
                elif user.is_authenticated and vendor_type.is_patient:
                    return redirect('profile')
                elif user.is_authenticated and vendor_type.is_lab:
                    return redirect('contact')
            else:
                return render(request, 'login.html', {'form':form})
        else:
            return render(request, 'login.html', {'form':form})

@method_decorator(login_required, name='dispatch')
class AddProfile(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            u_a_d = user_additional_detail.objects.get(user_id=user)
            form = AddProfileForm(initial={'address':u_a_d.address, 'mobile_number':u_a_d.mobile_number, 'phone_number':u_a_d.phone_number})
            return render(request, 'add-to-profile.html', {'form':form})

    def post(self, request):
        user = User.objects.get(username=request.user)
        obj= get_object_or_404(user_additional_detail, user_id=user.id)
        form = AddProfileForm(data=request.POST,files=request.FILES,instance= obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations! Your Profile is Successfully Updated")
        return render(request, 'add-to-profile.html', {'form':form})

@login_required
def profile(request):
    data = user_additional_detail.objects.get(user_id=request.user)
    return render(request, 'profile.html', {'data':data})

def searchreport(request):
    return render(request, 'search_report.html')

def search(request):
    if request.method == "POST":
        searched_id = request.POST['searched_id']
        searched_number = request.POST['searched_number']
        search_result = Report.objects.filter(Q(report_id__contains = searched_id) & Q(patient_mobile_number__contains = searched_number))
        if search_result:
            return render(request, 'search.html', {'search_result':search_result, 'search_id':searched_id, 'search_number':searched_number})
        else:
            return render(request, 'blank_page.html')

def yourreports(request):
    user = User.objects.get(username=request.user)
    report_by_other = Report.objects.filter(Q(patient_name__contains = request.user.first_name) & Q(patient_name__contains = request.user.last_name) & ~Q(user = user.id))
    report_by_user = Report.objects.filter(user = user.id)
    return render(request, 'your_reports.html', {'report':report_by_other, 'user_report':report_by_user })

def delete(request, pk):
    report_to_delete = Report.objects.get(pk=pk)
    report_to_delete.delete()
    return redirect('your-reports')

@login_required
def doctorrefferals(request):
    user = User.objects.get(username=request.user)
    user_type = user_additional_detail.objects.get(user_id=user)
    if request.user.is_authenticated and user_type.is_doctor:
        refferals = Report.objects.filter(Q(reffered_by__contains= request.user.first_name) & Q(reffered_by__contains= request.user.last_name))
        filter = DoctorFilter(request.GET, queryset=refferals)
        new_refferals = filter.qs
        return render(request, 'myrefferals_doctor.html', {'doctor':new_refferals, 'filter':filter, 'refferals':refferals})
    else:
        return render(request, 'restricted_user.html')

@login_required
def labrefferals(request):
    user = User.objects.get(username=request.user)
    user_type = user_additional_detail.objects.get(user_id=user)
    if request.user.is_authenticated and user_type.is_lab:
        report_made = Report.objects.filter(Q(user = request.user) & Q(lab_name__contains = user_type.lab_name))
        filter = LabFilter(request.GET, queryset=report_made)
        new_report_made = filter.qs
        return render(request, 'myrefferals_lab.html', {'lab':new_report_made, 'filter':filter, 'report':report_made})
    else:
        return render(request, 'restricted_user.html')


def FAQ(request):
    query_answers = Answer.objects.all()
    return render(request, 'FAQ.html', {'answers':query_answers})



@method_decorator(login_required, name='dispatch')
class ReportUpload(View):
    def get(self, request):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user)
            u_a_d = user_additional_detail.objects.get(user_id=user)
            if u_a_d.is_doctor:
                form = ReportUploadForm(initial={'reffered_by':f"{u_a_d.user_id.first_name} {u_a_d.user_id.last_name}"})
                form.fields['reffered_by'].widget.attrs.update({'readonly':True})
            elif u_a_d.is_lab:
                form = ReportUploadForm(initial={'lab_name':u_a_d.lab_name,})
                form.fields['lab_name'].widget.attrs.update({'readonly':True})
            else:
                form = ReportUploadForm()
        return render(request, 'upload_report.html', {'form':form})
    
    def post(self, request):
        form = ReportUploadForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = request.user
            if form.cleaned_data['report_id']=='':
                # generating report id if not exist using mobile number(last 4 digit)
                # and name of first name and date-time
                report_id = f"""{str(form.cleaned_data['patient_mobile_number'])[-4:]}{form.cleaned_data['patient_name'].split()[0].lower()}{datetime.datetime.now().strftime('%Y%m%d%H%M')}"""
            else:
                report_id=form.cleaned_data['report_id']
            report_name = form.cleaned_data['report_name']
            reffered_by = form.cleaned_data['reffered_by']
            lab_name = form.cleaned_data['lab_name']
            patient_name = form.cleaned_data['patient_name']
            patient_mobile_number = form.cleaned_data['patient_mobile_number']
            lab_mobile_number = form.cleaned_data['lab_mobile_number']
            report_upload = request.FILES['report_upload']
            try:
                report_image = request.FILES['report_image']
                img_ext = (report_image.name).split(".")[-1]
                custom_name_img = str(report_id)+'_' + str(lab_name).replace(" ", "")+'_' \
                         + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+'.'+img_ext
                report_image.name = custom_name_img.lower()
            except (KeyError,ValueError):
                custom_name_img = None
                report_image = None
            # building customize name using username_reportId_labName_patientName
            file_ext = (report_upload.name).split(".")[-1]
            
            custom_name_file = str(report_id)+'_' + str(lab_name).replace(" ", "")+'_' \
                         + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')+'.'+file_ext
            report_upload.name = custom_name_file.lower()
            
            add = Report(user=user, report_id=report_id, report_name=report_name, lab_name=lab_name,reffered_by=reffered_by ,patient_name=patient_name,patient_mobile_number=patient_mobile_number,
                        lab_mobile_number=lab_mobile_number, report_upload=report_upload,report_file_name=custom_name_file.lower(), report_image=report_image, report_img_name=custom_name_img.lower() if custom_name_img else None)
            add.save()
            messages.success(request, f"You Report has been successfully Uploaded. Report ID- {report_id}. Please Note It Down")
        return render(request, 'upload_report.html', {'form':form})
