from django.utils import timezone
from django.http import HttpResponse
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
import io
from django.shortcuts import render, redirect, reverse
from . import forms, models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta, date
from django.conf import settings
from django.db.models import Q
from django.contrib import messages
# timezone import
from django.utils import timezone
# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/index.html')

#for showing signup/login button for admin(by sumit)
def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/adminclick.html')

#for showing signup/login button for admin(by sumit)
def frontdeskclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/frontdeskclick.html')

#for showing signup/login button for doctor(by sumit)
def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/doctorclick.html')

#for showing signup/login button for admin(by sumit)
def dataentryclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/dataentryclick.html')

#for showing signup/login button for patient(by sumit)
def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/patientclick.html')

def admin_signup_view(request):
    form=forms.AdminSigupForm()
    if request.method=='POST':
        form=forms.AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()
            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)
            return HttpResponseRedirect('adminlogin')
    return render(request,'hospital/adminsignup.html',{'form':form})




def doctor_signup_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor=doctor.save()
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('doctorlogin')
    return render(request,'hospital/doctorsignup.html',context=mydict)


def patient_signup_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient=patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('patientlogin')
    return render(request,'hospital/patientsignup.html',context=mydict)


#-----------for checking user is doctor , patient or admin(by sumit)
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_frontdeskoperator(user):
    return user.groups.filter(name='FRONTDESK').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()
def is_dataentryoperator(user):
    return user.groups.filter(name='DATAENTRY').exists()


#---------AFTER ENTERING CREDENTIALS WE CHECK WHETHER USERNAME AND PASSWORD IS OF ADMIN,DOCTOR OR PATIENT
def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id)
        if accountapproval:
            return redirect('doctor-dashboard')
        else:
            return render(request,'hospital/doctor_wait_for_approval.html')
    # elif is_patient(request.user):
    #     accountapproval=models.Patient.objects.all().filter(user_id=request.user.id)
    #     if accountapproval:
    #         return redirect('patient-dashboard')
    #     else:
    #         return render(request,'hospital/patient_wait_for_approval.html')
    elif is_frontdeskoperator(request.user):
        accountapproval=models.FrontDeskOperator.objects.all().filter(user_id=request.user.id)
        if accountapproval:
            return redirect('frontdesk-dashboard')
        else:
            return render(request,'hospital/frontdesk_wait_for_approval.html')
    elif is_dataentryoperator(request.user):
        accountapproval=models.DataEntryOperator.objects.all().filter(user_id=request.user.id)
        if accountapproval:
            return redirect('dataentry-dashboard')
        else:
            return render(request,'hospital/dataentry_wait_for_approval.html')



#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    #for both table in admin dashboard
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')

    #adding shashwat
    frontdesk=models.FrontDeskOperator.objects.all().order_by('-id')
    dataentry=models.DataEntryOperator.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().count()
    #pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().count()
    admitted_patientcount= models.Patient.objects.all().filter(status=1).count
    #pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    frontdeskcount=models.FrontDeskOperator.objects.all().count()
    #pendingfrontdeskcount=models.FrontDeskOperator.objects.all().filter(status=False).count()

    dataentrycount=models.DataEntryOperator.objects.all().count()
    #pendingdataentrycount=models.DataEntryOperator.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().count()
    #pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'front_desk_operators': frontdesk,
    'data_entry_operators': dataentry,
    'doctorcount':doctorcount,
    'patientcount':patientcount,
    'admitted_patientcount': admitted_patientcount,
    'frontdeskcount':frontdeskcount,
    'dataentrycount':dataentrycount,
    'appointmentcount':appointmentcount,
    }
    return render(request,'hospital/admin_dashboard.html',context=mydict)


# this view for sidebar click on admin page
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'hospital/admin_doctor.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor.html',{'doctors':doctors})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_doctor_from_hospital_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-view-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)

    userForm=forms.DoctorUserForm(instance=user)
    doctorForm=forms.DoctorForm(request.FILES,instance=doctor)
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST,instance=user)
        doctorForm=forms.DoctorForm(request.POST,request.FILES,instance=doctor)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.status=True
            doctor.save()
            return redirect('admin-view-doctor')
    return render(request,'hospital/admin_update_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_doctor_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-doctor')
    return render(request,'hospital/admin_add_doctor.html',context=mydict)




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request):
    #those whose approval are needed
    doctors=models.Doctor.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_doctor.html',{'doctors':doctors})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-approve-doctor'))


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-approve-doctor')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_doctor_specialisation_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_doctor_specialisation.html',{'doctors':doctors})


#-----Admin user related to Front Desk Operator

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_frontdesk_view(request):
    return render(request,'hospital/admin_frontdesk.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_frontdesk_view(request):
    frontdesk=models.FrontDeskOperator.objects.all()
    return render(request,'hospital/admin_view_frontdesk.html',{'frontdesk':frontdesk})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_frontdesk_from_hospital_view(request,pk):
    frontdesk=models.FrontDeskOperator.objects.get(id=pk)
    user=models.User.objects.get(id=frontdesk.user_id)
    user.delete()
    frontdesk.delete()
    return redirect('admin-view-frontdesk')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_frontdesk_view(request,pk):
    frontdesk=models.FrontDeskOperator.objects.get(id=pk)
    user=models.User.objects.get(id=frontdesk.user_id)

    userForm=forms.FrontDeskUserForm(instance=user)
    frontdeskForm=forms.FrontDeskForm(request.FILES,instance=frontdesk)
    mydict={'userForm':userForm,'frontdeskForm':frontdeskForm}
    if request.method=='POST':
        userForm=forms.FrontDeskUserForm(request.POST,instance=user)
        frontdeskForm=forms.FrontDeskForm(request.POST,request.FILES,instance=frontdesk)
        if userForm.is_valid() and frontdeskForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            frontdesk=frontdeskForm.save(commit=False)
            frontdesk.save()
            return redirect('admin-view-frontdesk')
    return render(request,'hospital/admin_update_frontdesk.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_frontdesk_view(request):
    userForm=forms.FrontDeskUserForm()
    frontdeskForm=forms.FrontDeskForm()
    mydict={'userForm':userForm,'frontdeskForm':frontdeskForm}
    if request.method=='POST':
        userForm=forms.FrontDeskUserForm(request.POST)
        frontdeskForm=forms.FrontDeskForm(request.POST, request.FILES)
        if userForm.is_valid() and frontdeskForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            frontdesk=frontdeskForm.save(commit=False)
            frontdesk.user=user
            frontdesk.save()
            my_frontdesk_group = Group.objects.get_or_create(name='FRONTDESK')
            my_frontdesk_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-frontdesk')
    return render(request,'hospital/admin_add_frontdesk.html',context=mydict)

#-----Admin user related to Data Entry Operator

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dataentry_view(request):
    return render(request,'hospital/admin_dataentry.html')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_dataentry_view(request):
    dataentry=models.DataEntryOperator.objects.all()
    return render(request,'hospital/admin_view_dataentry.html',{'dataentry':dataentry})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_dataentry_from_hospital_view(request,pk):
    dataentry=models.DataEntryOperator.objects.get(id=pk)
    user=models.User.objects.get(id=dataentry.user_id)
    user.delete()
    dataentry.delete()
    return redirect('admin-view-dataentry')

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def update_dataentry_view(request,pk):
    dataentry=models.DataEntryOperator.objects.get(id=pk)
    user=models.User.objects.get(id=dataentry.user_id)

    userForm=forms.DataEntryUserForm(instance=user)
    dataentryForm=forms.DataEntryForm(request.FILES,instance=dataentry)
    mydict={'userForm':userForm,'dataentryForm':dataentryForm}
    if request.method=='POST':
        userForm=forms.DataEntryUserForm(request.POST,instance=user)
        dataentryForm=forms.DataEntryForm(request.POST,request.FILES,instance=dataentry)
        if userForm.is_valid() and dataentryForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            dataentry=dataentryForm.save(commit=False)
            dataentry.save()
            return redirect('admin-view-dataentry')
    return render(request,'hospital/admin_update_dataentry.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_dataentry_view(request):
    userForm=forms.DataEntryUserForm()
    dataentryForm=forms.DataEntryForm()
    mydict={'userForm':userForm,'dataentryForm':dataentryForm}
    if request.method=='POST':
        userForm=forms.DataEntryUserForm(request.POST)
        dataentryForm=forms.DataEntryForm(request.POST, request.FILES)
        print(userForm.is_valid())
        print(dataentryForm.is_valid())
        print(dataentryForm.errors.as_data())
        if userForm.is_valid() and dataentryForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            dataentry=dataentryForm.save(commit=False)
            dataentry.user=user
            dataentry.save()
            my_dataentry_group = Group.objects.get_or_create(name='DATAENTRY')
            my_dataentry_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-dataentry')
    return render(request,'hospital/admin_add_dataentry.html',context=mydict)

# --- Admin user related to patient below

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_patient_view(request):
    return render(request,'hospital/admin_patient.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_patient_view(request):
    patients=models.Patient.objects.all()
    return render(request,'hospital/admin_view_patient.html',{'patients':patients})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_patient_from_hospital_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-view-patient')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_update_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    patient_status=patient.status
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=patient_status
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('admin-view-patient')
    return render(request,'hospital/admin_update_patient.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_patient_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            patient=patientForm.save(commit=False)
            patient.user=user
            patient.status = 0
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-view-patient')
    return render(request,'hospital/admin_add_patient.html',context=mydict)



#------------------FOR APPROVING PATIENT BY ADMIN----------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_patient_view(request):
    #those whose approval are needed
    patients=models.Patient.objects.all().filter(status = 0)
    return render(request,'hospital/admin_approve_patient.html',{'patients':patients})


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    patient.status=True
    patient.save()
    return redirect(reverse('admin-approve-patient'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    user=models.User.objects.get(id=patient.user_id)
    user.delete()
    patient.delete()
    return redirect('admin-approve-patient')



#--------------------- FOR DISCHARGING PATIENT BY ADMIN START-------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_discharge_patient_view(request):
    patients=models.Patient.objects.all().filter(status=1)
    return render(request,'hospital/admin_discharge_patient.html',{'patients':patients})



@login_required(login_url='frontdesklogin')
@user_passes_test(is_frontdeskoperator)
def discharge_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    days=(date.today()-patient.admitDate) #2 days, 0:00:00
    assignedDoctor=models.User.objects.all().filter(id=patient.assignedDoctorId)
    d=days.days # only how many day that is 2
    patientDict={
        'patientId':pk,
        'name':patient.get_name,
        'mobile':patient.mobile,
        'address':patient.address,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'todayDate':date.today(),
        'day':d,
        'assignedDoctorName':assignedDoctor[0].first_name,
    }
    if request.method == 'POST':

        # set patient status to 2 (discharged)
        patient.status = 2
        patient.save()

        feeDict ={
            'roomCharge':int(request.POST['roomCharge'])*int(d),
            'doctorFee':request.POST['doctorFee'],
            'medicineCost' : request.POST['medicineCost'],
            'OtherCharge' : request.POST['OtherCharge'],
            'total':(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        }
        patientDict.update(feeDict)
        #for updating to database patientDischargeDetails (pDD)
        pDD=models.PatientDischargeDetails()
        pDD.patientId=pk
        pDD.patientName=patient.get_name
        pDD.assignedDoctorName=assignedDoctor[0].first_name
        pDD.address=patient.address
        pDD.mobile=patient.mobile
        pDD.symptoms=patient.symptoms
        pDD.admitDate=patient.admitDate
        pDD.releaseDate=date.today()
        pDD.daySpent=int(d)
        pDD.medicineCost=int(request.POST['medicineCost'])
        pDD.roomCharge=int(request.POST['roomCharge'])*int(d)
        pDD.doctorFee=int(request.POST['doctorFee'])
        pDD.OtherCharge=int(request.POST['OtherCharge'])
        pDD.total=(int(request.POST['roomCharge'])*int(d))+int(request.POST['doctorFee'])+int(request.POST['medicineCost'])+int(request.POST['OtherCharge'])
        pDD.save()
        return render(request,'hospital/patient_final_bill.html',context=patientDict)
    return render(request,'hospital/patient_generate_bill.html',context=patientDict)


#--------------for discharge patient bill (pdf) download and printing
import io
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse


def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = io.BytesIO()
    pdf = pisa.pisaDocument(io.BytesIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return



def download_pdf_view(request,pk):
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=pk).order_by('-id')[:1]
    dict={
        'patientName':dischargeDetails[0].patientName,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':dischargeDetails[0].address,
        'mobile':dischargeDetails[0].mobile,
        'symptoms':dischargeDetails[0].symptoms,
        'admitDate':dischargeDetails[0].admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
    }
    return render_to_pdf('hospital/download_bill.html',dict)



#-----------------APPOINTMENT START--------------------------------------------------------------------
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_appointment_view(request):
    return render(request,'hospital/admin_appointment.html')



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_view_appointment_view(request):
    appointments=models.Appointment.objects.all().filter(status=True)
    return render(request,'hospital/admin_view_appointment.html',{'appointments':appointments})



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm=forms.AppointmentForm()
    mydict={'appointmentForm':appointmentForm,}
    if request.method=='POST':
        appointmentForm=forms.AppointmentForm(request.POST)
        if appointmentForm.is_valid():
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.POST.get('patientId')
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=models.User.objects.get(id=request.POST.get('patientId')).first_name
            appointment.status=True
            appointment.save()
        return HttpResponseRedirect('admin-view-appointment')
    return render(request,'hospital/admin_add_appointment.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_add_appointment_view(request):
    appointmentForm = forms.AdminAppointmentForm()
    mydict = {'appointmentForm': appointmentForm, }

    if request.method == 'POST':
        if 'action' in request.POST and request.POST['action'] == 'check':
            appointment_time_str = request.POST.get('appointmentTime')
            appointment_time = timezone.make_aware(
                datetime.strptime(appointment_time_str, '%Y-%m-%dT%H:%M'))

            # Check which doctors are busy at the given appointmentTime
            busy_doctors = models.Appointment.objects.filter(
                appointmentTime=appointment_time).values_list('doctorId', flat=True).distinct()

            # Get a list of free doctors
            free_doctors = models.Doctor.objects.filter(
                ~Q(id__in=busy_doctors))

            print(
                f"The following doctors are busy at {appointment_time}: {list(busy_doctors)}")
            print(
                f"The following doctors are free at {appointment_time}: {list(free_doctors.values_list('id', flat=True))}")

            # Update the appointment form with free doctors queryset
            appointmentForm.fields['doctorId'].queryset = free_doctors

            context = {
                'appointmentForm': appointmentForm,
                'free_doctors': free_doctors,
            }

            return render(request, 'hospital/admin_add_appointment.html', context)

        else:
            appointmentForm = forms.AppointmentForm()
            mydict = {'appointmentForm': appointmentForm, }
            if request.method == 'POST':
                appointmentForm = forms.AppointmentForm(request.POST)
                if appointmentForm.is_valid():
                    doctor_id = request.POST.get('doctorId')
                    appointment_time = appointmentForm.cleaned_data.get(
                        'appointmentTime')
                    # Check if the selected doctor already has an appointment at the same time
                    if models.Appointment.objects.filter(doctorId=doctor_id, appointmentTime=appointment_time).exists():
                        messages.error(
                            request, 'The selected doctor already has an appointment scheduled at the same time.')
                        return redirect('admin-add-appointment')
                    appointment = appointmentForm.save(commit=False)
                    appointment.doctorId = doctor_id
                    appointment.patientId = request.POST.get('patientId')
                    appointment.doctorName = models.User.objects.get(
                        id=doctor_id).first_name
                    appointment.patientName = models.User.objects.get(
                        id=request.POST.get('patientId')).first_name
                    appointment.status = True
                    appointment.save()
                    messages.success(
                        request, 'Appointment added successfully!')
                    return redirect('admin-view-appointment')
            else:
                messages.error(
                    request, 'Invalid form submission. Please correct the errors below.')
    return render(request, 'hospital/admin_add_appointment.html', context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_appointment_view(request):
    #those whose approval are needed
    appointments=models.Appointment.objects.all().filter(status=False)
    return render(request,'hospital/admin_approve_appointment.html',{'appointments':appointments})


# ***** NEED TO MAKE CHANGES IN THIS FUNCTION ******
# ***** EXTRA SCHEDULING FUNCTION NEEDED, APPROVE/REJECT AFTER THAT *****
@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def approve_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.status=True
    appointment.save()
    return redirect(reverse('admin-approve-appointment'))



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def reject_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('admin-approve-appointment')
#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------






#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    #for three cards
    patientcount=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    appointmentcount=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).count()
    patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    #for  table in doctor dashboard
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id).order_by('-id')
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid).order_by('-id')
    appointments=zip(appointments,patients)
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'patientdischarged':patientdischarged,
    'appointments':appointments,
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_dashboard.html',context=mydict)



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_patient_view(request):
    mydict={
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_patient.html',context=mydict)




# ***** HERE, DOCTOR'S PRESCRIPTION FOR PATIENT MUST BE ADDED ******
@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_patient_view(request):
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def search_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    # whatever user write in search box we get in query
    query = request.GET['query']
    patients=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).filter(Q(symptoms__icontains=query)|Q(user__first_name__icontains=query))
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_discharge_patient_view(request):
    dischargedpatients=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name)
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_view_discharge_patient.html',{'dischargedpatients':dischargedpatients,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_appointment.html',{'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_delete_appointment_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})



@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
    appointments=zip(appointments,patients)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_write_prescription_view(request, pk):
    patient = models.Patient.objects.get(id=pk)
    # for profile picture of doctor in sidebar
    doctor = models.Doctor.objects.get(user_id=request.user.id)
    appointments = models.Appointment.objects.get(id=pk)

    print(patient)
    print(doctor)
    print(appointments)
    message = None
    form = forms.PrescriptionDoctorForm(instance=appointments)
    mydict = {
        'patient': patient,
        'form': form,
        'doctor': doctor,
        'message': message
    }
    if request.method == 'POST':
        form = forms.PrescriptionDoctorForm(
            request.POST, instance=appointments)
        if form.is_valid():
            form.save()

            return redirect('doctor-view-appointment')

    return render(request, 'hospital/doctor_write_prescription.html', context=mydict)

#---------------------------------------------------------------------------------
#------------------------ DOCTOR RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------


#---------------------------------------------------------------------------------
#------------------- FRONT DESK OPERATOR RELATED VIEWS START ---------------------
#---------------------------------------------------------------------------------
@login_required(login_url='frontdesklogin')
@user_passes_test(is_frontdeskoperator)
def frontdesk_dashboard_view(request):
    mydict={
    'patient':models.Patient.objects.all(), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/frontdesk_dashboard.html', mydict)


@login_required(login_url='frontdesklogin')
@user_passes_test(is_frontdeskoperator)
def frontdesk_patient_view(request):
    patients=models.Patient.objects.all()
    return render(request,'hospital/frontdesk_view_patient.html',{'patients':patients})


@login_required(login_url='frontdesklogin')
@user_passes_test(is_frontdeskoperator)
def frontdesk_update_patient_view(request,pk):
    patient=models.Patient.objects.get(id=pk)
    patient_status=patient.status
    user=models.User.objects.get(id=patient.user_id)

    userForm=forms.PatientUserForm(instance=user)
    patientForm=forms.PatientForm(request.FILES,instance=patient)
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST,instance=user)
        patientForm=forms.PatientForm(request.POST,request.FILES,instance=patient)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.status=patient_status
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient.save()
            return redirect('frontdesk-view-patient')
    return render(request,'hospital/frontdesk_update_patient.html',context=mydict)


    
@login_required(login_url='frontdesklogin')
@user_passes_test(is_frontdeskoperator)
def frontdesk_register_patient_view(request):
    userForm = forms.PatientUserForm()
    patientForm = forms.PatientForm()
    mydict = {'userForm':userForm,'patientForm':patientForm}

    if request.method == 'POST':
        userForm = forms.PatientUserForm(request.POST)
        patientForm = forms.PatientForm(request.POST, request.FILES)
        
        print(userForm.is_valid())
        print(patientForm.is_valid())
        print(patientForm.errors.as_data())

        if userForm.is_valid() and patientForm.is_valid():
            print('\n\n\n\nHELLOOOOO\n\n\n\n')
            user = userForm.save()
            user.set_password(user.password)
            user.save()

            patient = patientForm.save(commit=False)
            patient.user = user
            patient.status = 0
            # patient.profile_pic = patientForm.profile_pic
            patient.assignedDoctorId = request.POST.get('assignedDoctorId')
            patient.save()

            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)

        return HttpResponseRedirect('frontdesk-dashboard')
    return render(request,'hospital/frontdesk_view_register_patient.html',context=mydict)

@login_required(login_url='frontdesklogin')
@user_passes_test(is_frontdeskoperator)
def frontdesk_admit_patient_view(request):
    patients=models.Patient.objects.all().filter(status = 0)
    return render(request,'hospital/frontdesk_view_admit_patient.html',{'patients':patients})

@login_required(login_url='frontdesklogin')
@user_passes_test(is_frontdeskoperator)
def admit_patient_view(request, pk):
    patient = models.Patient.objects.get(id = pk)
    patient.status = 1
    patient.save()
    return redirect(reverse('frontdesk-admit-patient'))

@login_required(login_url='frontdesklogin')
@user_passes_test(is_frontdeskoperator)
def frontdesk_discharge_patient_view(request):
    patients = models.Patient.objects.all().filter(status = 1)
    return render(request,'hospital/frontdesk_view_discharge_patient.html',{'patients':patients})


#---------------------------------------------------------------------------------
#------------------------ DATA ENTRY OPERATOR RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------

@login_required(login_url='dataentrylogin')
@user_passes_test(is_dataentryoperator)
def dataentry_dashboard_view(request):
    mydict={
    'patient':models.Patient.objects.all(), 
    }
    return render(request,'hospital/dataentry_dashboard.html', mydict)


@login_required(login_url='dataentrylogin')
@user_passes_test(is_dataentryoperator)
def dataentry_patient_view(request):
    patients=models.Patient.objects.all()
    return render(request,'hospital/dataentry_view_patient.html',{'patients':patients})



#---------------------------------------------------------------------------------
#------------------------ PATIENT RELATED VIEWS START ------------------------------
#---------------------------------------------------------------------------------
@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id)
    doctor=models.Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict={
    'patient':patient,
    'doctorName':doctor.get_name,
    'doctorMobile':doctor.mobile,
    'doctorAddress':doctor.address,
    'symptoms':patient.symptoms,
    'doctorDepartment':doctor.department,
    'admitDate':patient.admitDate,
    }
    return render(request,'hospital/patient_dashboard.html',context=mydict)



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'hospital/patient_appointment.html',{'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_book_appointment_view(request):
    appointmentForm=forms.PatientAppointmentForm()
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    message=None
    mydict={'appointmentForm':appointmentForm,'patient':patient,'message':message}
    if request.method=='POST':
        appointmentForm=forms.PatientAppointmentForm(request.POST)
        if appointmentForm.is_valid():
            print(request.POST.get('doctorId'))
            desc=request.POST.get('description')

            doctor=models.Doctor.objects.get(user_id=request.POST.get('doctorId'))
            
            appointment=appointmentForm.save(commit=False)
            appointment.doctorId=request.POST.get('doctorId')
            appointment.patientId=request.user.id #----user can choose any patient but only their info will be stored
            appointment.doctorName=models.User.objects.get(id=request.POST.get('doctorId')).first_name
            appointment.patientName=request.user.first_name #----user can choose any patient but only their info will be stored
            appointment.status=False
            appointment.save()
        return HttpResponseRedirect('patient-view-appointment')
    return render(request,'hospital/patient_book_appointment.html',context=mydict)



def patient_view_doctor_view(request):
    doctors=models.Doctor.objects.all().filter(status=True)
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    return render(request,'hospital/patient_view_doctor.html',{'patient':patient,'doctors':doctors})



def search_doctor_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    
    # whatever user write in search box we get in query
    query = request.GET['query']
    doctors=models.Doctor.objects.all().filter(status=True).filter(Q(department__icontains=query)| Q(user__first_name__icontains=query))
    return render(request,'hospital/patient_view_doctor.html',{'patient':patient,'doctors':doctors})




@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_view_appointment_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    appointments=models.Appointment.objects.all().filter(patientId=request.user.id)
    return render(request,'hospital/patient_view_appointment.html',{'appointments':appointments,'patient':patient})



@login_required(login_url='patientlogin')
@user_passes_test(is_patient)
def patient_discharge_view(request):
    patient=models.Patient.objects.get(user_id=request.user.id) #for profile picture of patient in sidebar
    dischargeDetails=models.PatientDischargeDetails.objects.all().filter(patientId=patient.id).order_by('-id')[:1]
    patientDict=None
    if dischargeDetails:
        patientDict ={
        'is_discharged':True,
        'patient':patient,
        'patientId':patient.id,
        'patientName':patient.get_name,
        'assignedDoctorName':dischargeDetails[0].assignedDoctorName,
        'address':patient.address,
        'mobile':patient.mobile,
        'symptoms':patient.symptoms,
        'admitDate':patient.admitDate,
        'releaseDate':dischargeDetails[0].releaseDate,
        'daySpent':dischargeDetails[0].daySpent,
        'medicineCost':dischargeDetails[0].medicineCost,
        'roomCharge':dischargeDetails[0].roomCharge,
        'doctorFee':dischargeDetails[0].doctorFee,
        'OtherCharge':dischargeDetails[0].OtherCharge,
        'total':dischargeDetails[0].total,
        }
        print(patientDict)
    else:
        patientDict={
            'is_discharged':False,
            'patient':patient,
            'patientId':request.user.id,
        }
    return render(request,'hospital/patient_discharge.html',context=patientDict)


#------------------------ PATIENT RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------








#---------------------------------------------------------------------------------
#------------------------ ABOUT US AND CONTACT US VIEWS START ------------------------------
#---------------------------------------------------------------------------------
def aboutus_view(request):
    return render(request,'hospital/aboutus.html')

def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name=sub.cleaned_data['Name']
            message = sub.cleaned_data['Message']
            send_mail(str(name)+' || '+str(email),message,settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER, fail_silently = False)
            return render(request, 'hospital/contactussuccess.html')
    return render(request, 'hospital/contactus.html', {'form':sub})


#---------------------------------------------------------------------------------
#------------------------ ADMIN RELATED VIEWS END ------------------------------
#---------------------------------------------------------------------------------



#Developed By : sumit kumar
#facebook : fb.com/sumit.luv
#Youtube :youtube.com/lazycoders
