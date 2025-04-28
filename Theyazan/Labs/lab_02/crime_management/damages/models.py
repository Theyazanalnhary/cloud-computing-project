from django.db import models
from crimes.models import Crime  # استيراد نموذج الجريمة

class Damage(models.Model):
    damage_id = models.AutoField(primary_key=True, verbose_name="رقم الضرر")  # المفتاح الأساسي
    crime = models.ForeignKey(Crime, on_delete=models.CASCADE, related_name="damages", verbose_name="الجريمة")  # المفتاح الخارجي
    damage_type = models.CharField(max_length=50, choices=[('بشري', 'بشري'), ('مادي', 'مادي')], verbose_name="نوع الضرر")
    male_deaths = models.PositiveIntegerField(blank=True, null=True, verbose_name="عدد وفيات الذكور")
    female_deaths = models.PositiveIntegerField(blank=True, null=True, verbose_name="عدد وفيات الإناث")
    male_injuries = models.PositiveIntegerField(blank=True, null=True, verbose_name="عدد إصابات الذكور")
    female_injuries = models.PositiveIntegerField(blank=True, null=True, verbose_name="عدد إصابات الإناث")
    material_damage_description = models.TextField(blank=True, null=True, verbose_name="وصف الضرر المادي")

    def __str__(self):
        return f"ضرر رقم: {self.damage_id}"
    def __str__(self):
        return f"{self.damage_type} - {self.crime.report_number}"
    class Meta:
        unique_together = ('crime', 'damage_type', 'male_deaths','female_deaths')  # منع التكرار
        verbose_name = "ضرر"
        verbose_name_plural = "الأضرار"
    
        

