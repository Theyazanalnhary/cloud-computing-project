import requests
from django.conf import settings

class SMSNotifier:
    @staticmethod
    def send_sms(phone_number, message):
        # مثال باستخدام Twilio
        url = f'https://api.twilio.com/2010-04-01/Accounts/{settings.TWILIO_ACCOUNT_SID}/Messages.json'
        data = {
            'To': phone_number,
            'From': settings.TWILIO_PHONE_NUMBER,
            'Body': message
        }
        auth = (settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        try:
            response = requests.post(url, data=data, auth=auth)
            return response.status_code == 201
        except Exception as e:
            print(f"SMS sending failed: {str(e)}")
            return False

def notify_assigned_officer(report):
    if report.assigned_to and report.assigned_to.phone_number:
        message = f"تم تعيين بلاغ جديد لك: {report.title}"
        SMSNotifier.send_sms(report.assigned_to.phone_number, message) 