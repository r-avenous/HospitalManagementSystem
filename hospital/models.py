from django.db import models
from django.contrib.auth.models import User



departments=[('Cardiologist','Cardiologist'),
('Dermatologists','Dermatologists'),
('Emergency Medicine Specialists','Emergency Medicine Specialists'),
('Allergists/Immunologists','Allergists/Immunologists'),
('Anesthesiologists','Anesthesiologists'),
('Colon and Rectal Surgeons','Colon and Rectal Surgeons')
]

class Admin(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    # profile_pic = models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{}".format(self.user.first_name)
    
class FrontDeskOperator(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/FrontDeskOperatorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{}".format(self.user.first_name)

class DataEntryOperator(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/DataEntryOperatorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)

    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{}".format(self.user.first_name)

class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department= models.CharField(max_length=50,choices=departments,default='Cardiologist')
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)



class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    symptoms = models.CharField(max_length=100,null=False)
    assignedDoctorId = models.PositiveIntegerField(null=True)
    admitDate=models.DateField(auto_now=True, null=True)
    dischargeDate=models.DateField(auto_now=True, null=True)
    status=models.PositiveIntegerField(default = 0)
    room=models.PositiveIntegerField(null=True)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"


class Appointment(models.Model):
    Regular = 1
    Emergency = 2

    PRIORITY_CHOICES = [
        (Regular, 'Regular'),
        (Emergency, 'Emergency'),
    ]
    patientId = models.PositiveIntegerField(null=True)
    doctorId = models.PositiveIntegerField(null=True, blank=True)
    patientName = models.CharField(max_length=40, null=True)
    doctorName = models.CharField(max_length=40, null=True, blank=True)
    appointmentTime = models.DateTimeField(null=True)
    description = models.TextField(max_length=500)
    status = models.BooleanField(default=False)
    prescription = models.TextField(max_length=500)
    priority = models.IntegerField(choices=PRIORITY_CHOICES, null=True)



class PatientDischargeDetails(models.Model):
    patientId=models.PositiveIntegerField(null=True)
    patientName=models.CharField(max_length=40)
    assignedDoctorName=models.CharField(max_length=40)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    symptoms = models.CharField(max_length=100,null=True)

    admitDate=models.DateField(null=False)
    releaseDate=models.DateField(null=False)
    daySpent=models.PositiveIntegerField(null=False)

    roomCharge=models.PositiveIntegerField(null=False)
    medicineCost=models.PositiveIntegerField(null=False)
    doctorFee=models.PositiveIntegerField(null=False)
    OtherCharge=models.PositiveIntegerField(null=False)
    total=models.PositiveIntegerField(null=False)
    

# Changes made by Divyansh
class Procedure(models.Model):
    name = models.CharField(max_length=40)
    # id = models.PositiveIntegerField(null = False)
    cost = models.PositiveIntegerField(null=True)
    @property
    def get_name(self):
        return self.name
    @property 
    def get_id(self): 
        return self.id 
    def get_cost(self): 
        return self.cost
    

class Room(models.Model): 
    number = models.PositiveIntegerField(primary_key=True) 
    room_type = models.CharField(max_length=40) 
    available = models.BooleanField(default=True) 
    @property 
    def is_available(self): 
        return self.available
    

class Undergoes(models.Model): 
    #need help 
    patientId=models.ForeignKey(Patient, null=False, default=0, verbose_name="id", on_delete=models.SET_DEFAULT)  
    #need help 
    doctorId=models.ForeignKey(Doctor, null=False, default=0, verbose_name="id", on_delete=models.SET_DEFAULT)    
    procedureId= models.ForeignKey(Procedure, null=False, default=0, verbose_name="id", on_delete=models.SET_DEFAULT) 
    start_time=models.DateTimeField(null=False) 
    end_time=models.DateTimeField(null=False) 
    @property 
    def get_start_time(self): 
        return self.start_time 
    def get_end_time(self): 
        return self.end_time   