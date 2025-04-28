from django.db import models
from django.utils import timezone

class ArchiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_archived=True)

class ArchivedReport(models.Model):
    report = models.OneToOneField('CrimeReport', on_delete=models.CASCADE)
    archived_date = models.DateTimeField(auto_now_add=True)
    archived_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    archive_reason = models.TextField()
    
    objects = ArchiveManager()
    
    @classmethod
    def archive_report(cls, report, user, reason):
        report.is_archived = True
        report.save()
        
        return cls.objects.create(
            report=report,
            archived_by=user,
            archive_reason=reason
        ) 