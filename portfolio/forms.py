from django import forms
from django.core.validators import validate_email
from .models import ContactMessage
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML
from crispy_forms.bootstrap import FormActions


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full glass-light rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition',
                'placeholder': 'Your name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full glass-light rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition',
                'placeholder': 'your.email@example.com'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full glass-light rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition',
                'placeholder': 'What\'s this about?'
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full glass-light rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition',
                'rows': 5,
                'placeholder': 'Tell me about your project...'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'contact-form'
        self.helper.form_id = 'contact-form'
        
        # Add required field indicators
        for field_name, field in self.fields.items():
            field.required = True
            if field_name == 'message':
                field.help_text = 'Minimum 10 characters'
        
        self.helper.layout = Layout(
            Div(
                Div(
                    Field('name', wrapper_class='mb-6'),
                    css_class='md:w-1/2 md:pr-3'
                ),
                Div(
                    Field('email', wrapper_class='mb-6'),
                    css_class='md:w-1/2 md:pl-3'
                ),
                css_class='md:flex'
            ),
            Field('subject', wrapper_class='mb-6'),
            Field('message', wrapper_class='mb-8'),
            Submit(
                'submit',
                'Send Message',
                css_class='w-full md:w-auto px-8 py-3.5 bg-gradient-to-r from-purple-600 to-indigo-600 rounded-lg font-medium hover:from-purple-700 hover:to-indigo-700 transition flex items-center justify-center'
            )
        )
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError('Name must be at least 2 characters long.')
        if not name.replace(' ', '').isalpha():
            raise forms.ValidationError('Name should only contain letters and spaces.')
        return name
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except forms.ValidationError:
            raise forms.ValidationError('Please enter a valid email address.')
        return email.lower()
    
    def clean_subject(self):
        subject = self.cleaned_data.get('subject')
        if len(subject) < 5:
            raise forms.ValidationError('Subject must be at least 5 characters long.')
        return subject
    
    def clean_message(self):
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError('Message must be at least 10 characters long.')
        
        # Basic spam detection
        spam_keywords = ['viagra', 'casino', 'lottery', 'winner', 'claim now']
        message_lower = message.lower()
        for keyword in spam_keywords:
            if keyword in message_lower:
                raise forms.ValidationError('Your message contains prohibited content.')
        
        return message


class NewsletterForm(forms.Form):
    """Optional newsletter signup form"""
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'glass-light rounded-lg px-4 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500 transition',
            'placeholder': 'your.email@example.com'
        })
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'newsletter-form flex gap-2'
        
        self.helper.layout = Layout(
            Field('email', wrapper_class='flex-1'),
            Submit(
                'subscribe',
                'Subscribe',
                css_class='px-4 py-2 bg-gradient-to-r from-purple-600 to-indigo-600 rounded-lg font-medium hover:from-purple-700 hover:to-indigo-700 transition'
            )
        )
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except forms.ValidationError:
            raise forms.ValidationError('Please enter a valid email address.')
        return email.lower()
