from django.contrib import admin
from .models import FrontDeskOperator, DataEntryOperator, Doctor, Patient, Appointment, PatientDischargeDetails
# Register your models here.

class FrontDeskOperatorAdmin(admin.ModelAdmin):
    pass
admin.site.register(FrontDeskOperator, FrontDeskOperatorAdmin)

class DataEntryOperatorAdmin(admin.ModelAdmin):
    pass
admin.site.register(DataEntryOperator, DataEntryOperatorAdmin)

class DoctorAdmin(admin.ModelAdmin):
    pass
admin.site.register(Doctor, DoctorAdmin)

class PatientAdmin(admin.ModelAdmin):
    pass
admin.site.register(Patient, PatientAdmin)

class AppointmentAdmin(admin.ModelAdmin):
    pass
admin.site.register(Appointment, AppointmentAdmin)

class PatientDischargeDetailsAdmin(admin.ModelAdmin):
    pass
admin.site.register(PatientDischargeDetails, PatientDischargeDetailsAdmin)
