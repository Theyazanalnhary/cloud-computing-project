from django.db import models
from datetime import date, timedelta

class Donor(models.Model):
    GENDER_CHOICES = [('ذكر', 'Male'), ('انثى', 'Female')]
    BLOOD_TYPE_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), 
        ('AB+', 'AB+'), ('AB-', 'AB-'), ('O+', 'O+'), ('O-', 'O-')
    ]
    HEALTH_STATUS_CHOICES = [('معتمد', 'Approved'), ('غير معتمد', 'Not Approved')]

    full_name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=5, choices=GENDER_CHOICES)
    blood_type = models.CharField(max_length=3, choices=BLOOD_TYPE_CHOICES)
    phone_number = models.CharField(max_length=20)
    address = models.TextField()
    health_status = models.CharField(max_length=20, choices=HEALTH_STATUS_CHOICES)
    last_donation_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.full_name

    def save(self, *args, **kwargs):
        # تحقق من أن عمر المتبرع لا يقل عن 18 عامًا
        if (date.today() - self.date_of_birth).days < 18 * 365:
            raise ValueError("يجب أن يكون عمر المتبرع لا يقل عن 18 عامًا")

        super().save(*args, **kwargs)

    def update_last_donation_date(self, donation_date):
        """تحديث تاريخ آخر تبرع عند إضافة تبرع جديد"""
        self.last_donation_date = donation_date
        self.save()

    def can_donate_again(self):
        """التحقق من أن المتبرع يمكنه التبرع بعد انقضاء فترة بين التبرعات"""
        if self.last_donation_date:
            # تحديد فترة التبرع (على سبيل المثال 3 أشهر)
            min_donation_gap = timedelta(days=90)
            return date.today() - self.last_donation_date >= min_donation_gap
        return True  # إذا لم يكن هناك تبرع سابق، يمكن التبرع بحرية
