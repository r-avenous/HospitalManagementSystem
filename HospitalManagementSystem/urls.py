from django.contrib import admin
from django.urls import path
from hospital import views
from django.contrib.auth.views import LoginView,LogoutView

#-------------FOR ADMIN RELATED URLS
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_view,name=''),
    path('home',views.display_card_view),

    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),

    path('adminclick', views.adminclick_view),
    path('frontdeskclick', views.frontdeskclick_view),
    path('doctorclick', views.doctorclick_view),
    path('patientclick', views.patientclick_view),
    path('dataentryclick', views.dataentryclick_view),

    path('adminsignup', views.admin_signup_view),
    # path('doctorsignup', views.doctor_signup_view,name='doctorsignup'),
    # path('patientsignup', views.patient_signup_view),
    
    path('adminlogin', LoginView.as_view(template_name='hospital/adminlogin.html')),
    path('frontdesklogin', LoginView.as_view(template_name='hospital/frontdesklogin.html')),
    path('doctorlogin', LoginView.as_view(template_name='hospital/doctorlogin.html')),
    path('patientlogin', LoginView.as_view(template_name='hospital/patientlogin.html')),
    path('dataentrylogin', LoginView.as_view(template_name='hospital/dataentrylogin.html')),

    path('afterlogin', views.afterlogin_view,name='afterlogin'),
    path('logout/', LogoutView.as_view(template_name='hospital/index.html'),name='logout'),


    path('admin-dashboard', views.admin_dashboard_view,name='admin-dashboard'),

    path('admin-doctor', views.admin_doctor_view,name='admin-doctor'),
    path('admin-view-doctor', views.admin_view_doctor_view,name='admin-view-doctor'),
    path('delete-doctor-from-hospital/<int:pk>', views.delete_doctor_from_hospital_view,name='delete-doctor-from-hospital'),
    path('update-doctor/<int:pk>', views.update_doctor_view,name='update-doctor'),
    path('admin-add-doctor', views.admin_add_doctor_view,name='admin-add-doctor'),
    #path('admin-approve-doctor', views.admin_approve_doctor_view,name='admin-approve-doctor'),
    #path('approve-doctor/<int:pk>', views.approve_doctor_view,name='approve-doctor'),
    #path('reject-doctor/<int:pk>', views.reject_doctor_view,name='reject-doctor'),
    #path('admin-view-doctor-specialisation',views.admin_view_doctor_specialisation_view,name='admin-view-doctor-specialisation'),

    path('admin-frontdesk', views.admin_frontdesk_view,name='admin-frontdesk'),
    path('admin-view-frontdesk', views.admin_view_frontdesk_view, name='admin-view-frontdesk'),
    path('delete-frontdesk-from-hospital/<int:pk>', views.delete_frontdesk_from_hospital_view,name='delete-frontdesk-from-hospital'),
    path('update-frontdesk/<int:pk>', views.update_frontdesk_view,name='update-frontdesk'),
    path('admin-add-frontdesk', views.admin_add_frontdesk_view,name='admin-add-frontdesk'),
    
    #urls for admin related to dataentry

    path('admin-dataentry', views.admin_dataentry_view,name='admin-dataentry'),
    path('admin-view-dataentry', views.admin_view_dataentry_view, name='admin-view-dataentry'),
    path('delete-dataentry-from-hospital/<int:pk>', views.delete_dataentry_from_hospital_view,name='delete-dataentry-from-hospital'),
    path('update-dataentry/<int:pk>', views.update_dataentry_view,name='update-dataentry'),
    path('admin-add-dataentry', views.admin_add_dataentry_view,name='admin-add-dataentry'),

    path('admin-patient', views.admin_patient_view,name='admin-patient'),
    path('admin-view-patient', views.admin_view_patient_view,name='admin-view-patient'),
    path('delete-patient-from-hospital/<int:pk>', views.delete_patient_from_hospital_view,name='delete-patient-from-hospital'),
    path('admin-update-patient/<int:pk>', views.admin_update_patient_view,name='admin-update-patient'),
    path('admin-add-patient', views.admin_add_patient_view,name='admin-add-patient'),
    #path('admin-approve-patient', views.admin_approve_patient_view,name='admin-approve-patient'),
    #path('approve-patient/<int:pk>', views.approve_patient_view,name='approve-patient'),
    #path('reject-patient/<int:pk>', views.reject_patient_view,name='reject-patient'),
    path('admin-discharge-patient', views.admin_discharge_patient_view,name='admin-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view,name='discharge-patient'),
    path('download-pdf/<int:pk>', views.download_pdf_view,name='download-pdf'),


    path('admin-appointment', views.admin_appointment_view,name='admin-appointment'),
    path('admin-view-appointment', views.admin_view_appointment_view,name='admin-view-appointment'),
    path('admin-add-appointment', views.admin_add_appointment_view,name='admin-add-appointment'),
    path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
    path('approve-appointment/<int:pk>', views.approve_appointment_view,name='approve-appointment'),
    path('reject-appointment/<int:pk>', views.reject_appointment_view,name='reject-appointment'),
]


#---------FOR DOCTOR RELATED URLS-------------------------------------
urlpatterns +=[
    path('doctor-dashboard', views.doctor_dashboard_view,name='doctor-dashboard'),
    path('search', views.search_view,name='search'),

    path('doctor-patient', views.doctor_patient_view,name='doctor-patient'),
    path('doctor-view-patient', views.doctor_view_patient_view,name='doctor-view-patient'),
    path('doctor-view-test/<int:pk>', views.doctor_view_test_view,name='doctor-view-test'),
    path('doctor-view-test-details/<int:pk>', views.doctor_view_test_details_view,name='doctor-view-test-details'),
    path('doctor-view-discharge-patient',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),

    path('doctor-appointment', views.doctor_appointment_view,name='doctor-appointment'),
    path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
    path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
    path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
    path('doctor-write-prescription/<int:pk>', views.doctor_write_prescription_view,
         name='doctor-write-prescription'),
]

#---------FOR DATA ENTRY OPERATOR RELATED URLS-------------------------------------
urlpatterns +=[
    path('dataentry-dashboard', views.dataentry_dashboard_view,name='dataentry-dashboard'),
    path('dataentry-view-test', views.dataentry_test_view,name='dataentry-view-test'),
    path('dataentry-add-test', views.dataentry_add_test_view,name='dataentry-add-test'),
    path('dataentry-add-test-hospital', views.dataentry_add_test_hospital_view,name='dataentry-add-test-hospital'),
    path('dataentry-add-test-others', views.dataentry_add_test_others_view,name='dataentry-add-test-others'),
    path('dataentry-update-test/<int:pk>', views.dataentry_update_test_view,name='dataentry-update-test'),
    path('dataentry-delete-test/<int:pk>', views.dataentry_delete_test_view,name='dataentry-delete-test'),
#     path('search', views.search_view,name='search'),

#     path('doctor-patient', views.doctor_patient_view,name='doctor-patient'),
#     path('doctor-view-patient', views.doctor_view_patient_view,name='doctor-view-patient'),
#     path('doctor-view-discharge-patient',views.doctor_view_discharge_patient_view,name='doctor-view-discharge-patient'),
#     path('doctor-appointment', views.doctor_appointment_view,name='doctor-appointment'),
#     path('doctor-view-appointment', views.doctor_view_appointment_view,name='doctor-view-appointment'),
#     path('doctor-delete-appointment',views.doctor_delete_appointment_view,name='doctor-delete-appointment'),
#     path('delete-appointment/<int:pk>', views.delete_appointment_view,name='delete-appointment'),
#     path('doctor-write-prescription/<int:pk>', views.doctor_write_prescription_view,
#          name='doctor-write-prescription'),
]

#---------FOR FRONT DESK OPERATOR RELATED URLS-------------------------

urlpatterns +=[

    path('frontdesk-dashboard', views.frontdesk_dashboard_view,name='frontdesk-dashboard'),
    path('frontdesk-view-patient', views.frontdesk_patient_view,name='frontdesk-view-patient'),
    path('frontdesk-update-patient/<int:pk>', views.frontdesk_update_patient_view,name='frontdesk-update-patient'),
    path('frontdesk-register-patient', views.frontdesk_register_patient_view,name='frontdesk-register-patient'),
    path('frontdesk-admit-patient',views.frontdesk_admit_patient_view,name='frontdesk-admit-patient'),
    path('admit-patient-option/<int:pk>',views.admit_patient_option_view,name='admit-patient-option'),
    # path('admit-patient/<int:pk>', views.admit_patient_view,name='admit-patient'),
    path('admit-patient-private/<int:pk>', views.admit_patient_private_view,name='admit-patient-private'),
    path('admit-patient-general/<int:pk>', views.admit_patient_general_view,name='admit-patient-general'),
    path('frontdesk-discharge-patient',views.frontdesk_discharge_patient_view,name='frontdesk-discharge-patient'),
    path('discharge-patient/<int:pk>', views.discharge_patient_view,name='discharge-patient'),
    #path('frontdesk-appointment', views.frontdesk_appointment_view,name='admin-appointment'),
    path('frontdesk-view-appointment', views.frontdesk_appointment_view,name='frontdesk-view-appointment'),
    path('frontdesk-add-appointment', views.frontdesk_add_appointment,name='frontdesk-add-appointment'),
    path('frontdesk-update-appointment/<int:pk>', views.frontdesk_update_appointment_view,name='frontdesk-update-appointment'),
    path('frontdesk-delete-appointment/<int:pk>', views.frontdesk_delete_appointment,name='frontdesk-delete-appointment'),
    
    path('frontdesk-view-undergoes', views.frontdesk_undergoes_view,name='frontdesk-view-undergoes'),
    path('frontdesk-add-undergoes', views.frontdesk_add_undergoes,name='frontdesk-add-undergoes'),
    path('frontdesk-update-undergoes/<int:pk>', views.frontdesk_update_undergoes_view,name='frontdesk-update-undergoes'),
    path('frontdesk-delete-undergoes/<int:pk>', views.frontdesk_delete_undergoes,name='frontdesk-delete-undergoes'),
    #path('admin-approve-appointment', views.admin_approve_appointment_view,name='admin-approve-appointment'),
]


# ****************** ADD FIELD IN frontdesk-view-update-form for FDO to change status of patient
# ****************** ALLOWS PREVIOUS USERS (DISCHARGED) TO CHANGE TO VISITING WHEN THEY VISIT HOSPITAL AGAIN

#---------FOR PATIENT RELATED URLS-------------------------------------
urlpatterns +=[

    path('patient-dashboard', views.patient_dashboard_view,name='patient-dashboard'),
    path('patient-appointment', views.patient_appointment_view,name='patient-appointment'),
    path('patient-book-appointment', views.patient_book_appointment_view,name='patient-book-appointment'),
    path('patient-view-appointment', views.patient_view_appointment_view,name='patient-view-appointment'),
    path('patient-view-doctor', views.patient_view_doctor_view,name='patient-view-doctor'),
    path('searchdoctor', views.search_doctor_view,name='searchdoctor'),
    path('patient-discharge', views.patient_discharge_view,name='patient-discharge'),

]
