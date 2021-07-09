from django.db import models
from phone_field import PhoneField
from django.contrib.auth.models import User

# Create your models here.
CHOICES = (
    ("GEN", "GEN"),
    ("OBC", "OBC"),
    ("SC", "SC"),
    ("ST", "ST"),
    ("GENPWD", "GENPWD"),
    ("OBCPWD", "OBCPWD"),
    ("SCPWD", "SCPWD"),
    ("STPWD", "STPWD"),
)

CHOICES1 = (
    ("MALE", "MALE"),
    ("FEMALE", "FEMALE"),
    ("OTHER", "OTHER"),
)


class College(models.Model):
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name


class Branch(models.Model):
    name = models.CharField(max_length=100, null=False)
    college = models.ForeignKey(College, on_delete=models.CASCADE, null=False)
    capacity = models.IntegerField(default=50)
    preferences = models.CharField(max_length=1000, default="", null=True, blank=True)
    gen_capacity = models.IntegerField(default=0)
    gen_pwd_capacity = models.IntegerField(default=0)
    obc_ncl_capacity = models.IntegerField(default=0)
    obc_ncl_pwd_capacity = models.IntegerField(default=0)
    sc_capacity = models.IntegerField(default=0)
    sc_pwd_capacity = models.IntegerField(default=0)
    st_capacity = models.IntegerField(default=0)
    st_pwd_capacity = models.IntegerField(default=0)
    gen_capacity_filled = models.IntegerField(default=0)
    gen_pwd_capacity_filled = models.IntegerField(default=0)
    obc_ncl_capacity_filled = models.IntegerField(default=0)
    obc_ncl_pwd_capacity_filled = models.IntegerField(default=0)
    sc_capacity_filled = models.IntegerField(default=0)
    sc_pwd_capacity_filled = models.IntegerField(default=0)
    st_capacity_filled = models.IntegerField(default=0)
    st_pwd_capacity_filled = models.IntegerField(default=0)

    def setpreferences(self, x):
        self.preferences = ",".join(x)

    def getpreferences(self):
        return self.preferences.split(',')

    def __str__(self):
        return self.college.name + "-" + self.name


class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rollnumber = models.CharField(max_length=15, null=False, unique=True)
    category = models.CharField(max_length=100, choices=CHOICES, null=False)
    gender = models.CharField(max_length=100, choices=CHOICES1, null=False)
    rank = models.IntegerField(null=False, unique=True)
    birthdate = models.DateField(null=True, blank=True)
    email = models.EmailField(null=False)
    phone = PhoneField(null=False, blank=True)
    preferences = models.CharField(max_length=1000, default="", null=True, blank=True)
    freeze = models.IntegerField(default=0)
    locked = models.IntegerField(default=0)
    removed = models.IntegerField(default=0)
    is_admin = models.IntegerField(default=0)
    final_seat = models.ForeignKey(Branch, on_delete=models.CASCADE, null=True, blank=True)
    quota_for_seat = models.CharField(max_length=100, choices=CHOICES, blank=True)

    def setpreferences(self, x):
        self.preferences = ",".join(x)

    def getpreferences(self):
        return self.preferences.split(',')

    class Meta:
        ordering = ['rank']

    def __str__(self):
        return self.rollnumber
