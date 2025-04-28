from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import CrimeReport
from datetime import datetime

User = get_user_model()

class ReportTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            user_type='police'
        )
        self.client.login(username='testuser', password='testpass123')
        
        self.report = CrimeReport.objects.create(
            title='Test Report',
            description='Test Description',
            location='Test Location',
            date_occurred=datetime.now(),
            reporter_name='Test Reporter',
            reporter_phone='1234567890',
            reporter_email='test@example.com',
            assigned_to=self.user
        )
    
    def test_report_list_view(self):
        response = self.client.get(reverse('reports:list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Report')
    
    def test_report_detail_view(self):
        response = self.client.get(
            reverse('reports:detail', kwargs={'pk': self.report.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.report.title)
    
    def test_create_report(self):
        response = self.client.post(reverse('reports:create'), {
            'title': 'New Report',
            'description': 'New Description',
            'location': 'New Location',
            'date_occurred': datetime.now(),
            'reporter_name': 'New Reporter',
            'reporter_phone': '0987654321',
            'reporter_email': 'new@example.com',
            'priority': 'high'
        })
        self.assertEqual(response.status_code, 302)  # تم التحويل بنجاح
        self.assertTrue(
            CrimeReport.objects.filter(title='New Report').exists()
        ) 