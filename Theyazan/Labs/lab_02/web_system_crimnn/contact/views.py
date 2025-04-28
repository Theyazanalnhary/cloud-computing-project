from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import ContactMessage
from .forms import ContactForm

# Create your views here.

class ContactView(CreateView):
    model = ContactMessage
    form_class = ContactForm
    template_name = 'contacts/contact.html'
    success_url = reverse_lazy('contact_success')
