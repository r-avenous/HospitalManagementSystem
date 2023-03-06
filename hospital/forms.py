from django.forms import ModelChoiceField
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
from .models import Appointment, Doctor, Patient
from django import forms
from django.contrib.auth.models import User
from . import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
import datetime
from django.db.models import Q
from django.forms import ModelChoiceField
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime
#for admin signup
class AdminSigupForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }


#for student related form
class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoctorForm(forms.ModelForm):
    class Meta:
        model=models.Doctor
        fields=['address','mobile','department','status','profile_pic']
        
class PatientForm(forms.ModelForm):
    #this is the extrafield for linking patient and their assigned doctor
    #this will show dropdown __str__ method doctor model is shown on html so override it
    #to_field_name this will fetch corresponding value  user_id present in Doctor model and return it
    assignedDoctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Patient
        fields=['first_name', 'last_name', 'address', 'mobile', 'symptoms', 'profile_pic']

#adding shashwat
class FrontDeskUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class FrontDeskForm(forms.ModelForm):
    class Meta:
        model=models.FrontDeskOperator
        fields=['address','mobile','profile_pic']

class DataEntryUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class DataEntryForm(forms.ModelForm):
    class Meta:
        model=models.DataEntryOperator
        fields=['address','mobile','profile_pic']

# ending adding shashwat


class AppointmentForm(forms.ModelForm):
    patientId = forms.ModelChoiceField(queryset=Patient.objects.filter(Q(status=0) | Q(status=1)),
                                      empty_label="Patient Name and Symptoms",
                                        to_field_name="user_id",
                                      required=False)

    appointmentTime = forms.DateTimeField(input_formats=[
                                          '%Y-%m-%dT%H:%M'], widget=forms.DateTimeInput(format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}))
    priority = forms.ChoiceField(choices=Appointment.PRIORITY_CHOICES)

    class Meta:
        model = Appointment
        fields = ['description', 'status', 'priority', 'appointmentTime']


class AdminAppointmentForm(AppointmentForm):
    doctorId = forms.ModelChoiceField(queryset=Doctor.objects.filter(
        status=True), empty_label="Doctor Name and Department", to_field_name="user_id", required=False)


class PatientAppointmentForm(forms.ModelForm):
    doctorId=forms.ModelChoiceField(queryset=models.Doctor.objects.all().filter(status=True),empty_label="Doctor Name and Department", to_field_name="user_id")
    class Meta:
        model=models.Appointment
        fields=['description','status']
# Adding Yatharth


class PrescriptionDoctorForm(forms.ModelForm):
    class Meta:
        model = models.Appointment
        fields = ['prescription']
# Ending Yatharth
#for contact us page
class ContactusForm(forms.Form):
    Name = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Message = forms.CharField(max_length=500,widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
    
    
#for adding tests (only for admitted and visiting patients)
class TestForm1(forms.ModelForm):
    patientId = forms.ModelChoiceField(queryset=(models.Patient.objects.all().filter(status=0)|models.Patient.objects.all().filter(status=1)),empty_label="Patient Name", to_field_name="id",required=True)
    class Meta:
        model=models.Test
        fields = ['patientId', 'doctername', 'procedurename', 'description', 'image']

class TestForm2(forms.ModelForm):
    patientId = forms.ModelChoiceField(queryset=(models.Patient.objects.all().filter(status=0)|models.Patient.objects.all().filter(status=1)),empty_label="Patient Name", to_field_name="id",required=True)
    docterId = forms.ModelChoiceField(queryset=models.Doctor.objects.all(),empty_label="Docter Name", to_field_name="id",required=True)
    ProcedureId = forms.ModelChoiceField(queryset=models.Procedure.objects.all(), empty_label="Procedure Name", to_field_name="id",required=True)
    class Meta:
        model=models.Test
        fields = ['patientId', 'docterId', 'ProcedureId', 'description', 'image']
#form end



#Developed By : sumit kumar
#facebook : fb.com/sumit.luv
#Youtube :youtube.com/lazycoders
