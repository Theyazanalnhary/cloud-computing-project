from django.db import models

class Log(models.Model):
    log_id = models.AutoField(primary_key=True)
    employee_id = models.IntegerField()  # يمكن ربطه بـ Employee إذا كان لدينا نموذج Employee مرتبط بـ EmployeeID
    action = models.TextField()
    action_date = models.DateTimeField()

    def __str__(self):
        return f"Log {self.log_id}"
