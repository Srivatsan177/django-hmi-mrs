from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    age = models.IntegerField()
    gender = models.IntegerField()
    name = models.CharField(max_length=32)

    def __str__(self):
        return str(self.user)

class Medicine(models.Model):
    medicine_name = models.CharField(max_length=32)
    medicine_type = models.CharField(max_length=32)
    dose = models.IntegerField()
    # day = models.IntegerField(max_length=32)
    time = models.CharField(max_length=32)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    medicine_image = models.CharField(max_length=32)
    def __str__(self):
        return self.medicine_name

class MedicineDay(models.Model):
    day = models.IntegerField()
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.day)