from django import forms
import django_filters
from .models import *
from django_filters import DateFilter, CharFilter

class DoctorFilter(django_filters.FilterSet):
    start_date = DateFilter(label="Starting Date",field_name="create_date", lookup_expr='gte', widget=forms.DateInput(attrs={'class':'form-control', 'id':'datepicker', 'placeholder':'From Date' }))
    end_date = DateFilter(label="End Date",field_name="create_date", lookup_expr='lte', widget=forms.DateInput(attrs={'class':'form-control', 'id':'datepicker1', 'placeholder':'To Date'}))
    lab_name = CharFilter(label="Lab Name",lookup_expr='icontains',field_name="lab_name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Search by Lab Name'}))
    patient_name = CharFilter(label="Patient Name",lookup_expr='icontains',field_name="patient_name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Search by Patient Name'}))
    class Meta:
        model = Report
        fields = [ 'lab_name', 'patient_name']

class LabFilter(django_filters.FilterSet):
    start_date = DateFilter(label="Starting Date",field_name="create_date", lookup_expr='gte', widget=forms.DateInput(attrs={'class':'form-control','id':'datepicker2', 'placeholder':'From Date'}))
    end_date = DateFilter(label="End Date",field_name="create_date", lookup_expr='lte', widget=forms.DateInput(attrs={'class':'form-control','id':'datepicker3', 'placeholder':'To Date'}))
    reffered_by = CharFilter(label="Doctor Name",lookup_expr='icontains',field_name="reffered_by", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Search by Doctor Name'}))
    patient_name = CharFilter(label="Patient Name",lookup_expr='icontains',field_name="patient_name", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Search by Patient Name'}))
    class Meta:
        model = Report
        fields = [ 'reffered_by', 'patient_name']
       