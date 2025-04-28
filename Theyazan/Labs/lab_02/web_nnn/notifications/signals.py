from django.db.models.signals import post_save
from django.dispatch import receiver
from reports.models import CrimeReport, Evidence, Investigation
from .models import Notification

@receiver(post_save, sender=CrimeReport)
def create_report_notification(sender, instance, created, **kwargs):
    if created:
        if instance.assigned_to:
            Notification.objects.create(
                user=instance.assigned_to,
                notification_type='report_assigned',
                title='تم تعيين تقرير جديد لك',
                message=f'تم تعيين التقرير "{instance.title}" لك',
                related_link=f'/reports/{instance.pk}/'
            )

@receiver(post_save, sender=Evidence)
def create_evidence_notification(sender, instance, created, **kwargs):
    if created:
        report = instance.report
        if report.assigned_to:
            Notification.objects.create(
                user=report.assigned_to,
                notification_type='evidence_added',
                title='تم إضافة دليل جديد',
                message=f'تم إضافة دليل جديد للتقرير "{report.title}"',
                related_link=f'/reports/{report.pk}/'
            ) 