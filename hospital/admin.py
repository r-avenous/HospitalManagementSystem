from django.contrib import admin
from .models import Admin, FrontDeskOperator, DataEntryOperator, Doctor, Patient, Appointment, PatientDischargeDetails, Procedure, Room, Undergoes, Test
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

class AdminAdmin(admin.ModelAdmin):
    pass
admin.site.register(Admin,AdminAdmin)

class ProcedureAdmin(admin.ModelAdmin):
    pass
admin.site.register(Procedure,ProcedureAdmin)

class RoomAdmin(admin.ModelAdmin):
    pass
admin.site.register(Room,RoomAdmin)

class UndergoesAdmin(admin.ModelAdmin):
    pass
admin.site.register(Undergoes,UndergoesAdmin)

class TestAdmin(admin.ModelAdmin):
    pass
admin.site.register(Test,TestAdmin)
