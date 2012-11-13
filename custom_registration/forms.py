# -*- coding: utf-8 -*-
'''
Created on Mar 20, 2012

@author: Mourad Mourafiq

@copyright: Copyright © 2012

other contributers: Naamane othmane
'''

from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field,  Fieldset,Reset
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions
from cities.models import City
from utils.forms_util import CityModelChoiceField,MAPhoneNumberField


import datetime
GENDER = (    
    ('1', _('Homme')),
    ('2', _('Femme')),
    )

# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_dict = {'class': 'required'}






class RegistrationPatientForm(forms.Form):
    """
    Form for registering a new user account.
    
    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    
    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.
    
    """    
    last_name = forms.RegexField(regex=r'^[a-zA-Z]+$',
                                max_length=20,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Prénom"),
                                error_messages={'invalid': _(u"Seul les caractères sont autorisés.")})
    first_name = forms.RegexField(regex=r'^[a-zA-Z]+$',
                                max_length=20,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Nom"),
                                error_messages={'invalid': _(u"Seul les caractères sont autorises.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_("E-mail"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                min_length = 8,
                                error_messages={'invalid': _(u"Minimum 8 caractères.")},
                                label=_("Password"))
    '''
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password (again)"))
    '''
    birthday = forms.DateField(widget=forms.DateInput(),label=_("Date de naissance"))
    phone = MAPhoneNumberField(widget=forms.TextInput(attrs=attrs_dict),
                               error_messages={ 'invalid': _(u"Format incorrect")})
    city = CityModelChoiceField(label=_('Ville'), 
                                  queryset=City.objects.filter(active=True).order_by('country__id', 'slug'),
                                  empty_label=None)    
    gender = forms.ChoiceField(widget=forms.RadioSelect(), label=_('Sexe'), choices = GENDER)
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
                             label=_(u"J'accepte les Conditions d'utilisation et les règles de confidentialité de DocDoc."),
                             error_messages={ 'required': _(u"Vous devez accepter les conditions d'utilisations.")})
    honeypot = forms.CharField(required=False,
                                    label=_('If you enter anything in this field '\
                                            'your comment will be treated as spam'))  
        
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id_registration_patient'        
        self.helper.form_method = 'post'
        self.helper.form_action = 'registration_register_patient'
        self.helper.form_class = "form-horizontal"
        self.helper.error_text_inline = True
        self.helper.layout = Layout(                                                       
            'email',
            'password1',
            'last_name',
            'first_name',
            'birthday',
            'gender',
            'phone',
            'city',                
            'tos',
            'honeypot',
            FormActions(
                Submit('submit', 'Envoyer', css_class="btn-primary"),
                HTML('<a class="btn" href="/">Annuler</a>')         
                )
            )
        super(RegistrationPatientForm, self).__init__(*args, **kwargs)
        
    def clean_honeypot(self):
        """Check that nothing's been entered into the honeypot."""
        value = self.cleaned_data["honeypot"]
        if value:
            raise forms.ValidationError(self.fields["honeypot"].label)
        return value    
    
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']
    
    def clean_birthday(self):
        """birthdays should bigger than 13"""
        birthday = self.cleaned_data['birthday']
        if birthday:
            birthday = birthday.replace(year = (birthday.year + 13))
            if birthday > datetime.date.today():
                raise forms.ValidationError(_(u'You should be at least 13.'))
            else:
                return self.cleaned_data['birthday']
    '''
    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms. .ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data
    '''

    
class RegistrationDoctorForm(forms.Form):
    """
    Form for registering a new user account.
    
    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    
    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.
    
    """
    nom = forms.RegexField(regex=r'^[a-zA-Z]+$',
                                max_length=20,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Nom"),
                                error_messages={'invalid': _("Seul les caracteres sont autorises.")})
    prenom = forms.RegexField(regex=r'^[a-zA-Z]+$',
                                max_length=20,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Prenom"),
                                error_messages={'invalid': _("Seul les caracteres sont autorises.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_("E-mail"))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_("Password (again)"))
    
    def clean_username(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that username already exists."))
        else:
            return self.cleaned_data['username']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data

    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']