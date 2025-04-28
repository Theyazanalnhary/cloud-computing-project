from django.core.exceptions import ValidationError
from django.utils import timezone

def validate_future_date(value):
    if value > timezone.now():
        raise ValidationError('لا يمكن أن يكون تاريخ الحادثة في المستقبل')

def validate_coordinates(value):
    try:
        float_value = float(value)
        if float_value < -90 or float_value > 90:
            raise ValidationError('قيمة الإحداثيات غير صحيحة')
    except ValueError:
        raise ValidationError('يجب أن تكون الإحداثيات أرقاماً') 