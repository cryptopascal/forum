'''
Created on 14 nov. 2012

@author: naamane.othmane
'''

from django.contrib.auth.models import User
from django import forms
from django.utils.translation import ugettext_lazy as _
from my_forum.models import Thread,Post
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,  Submit, HTML
from crispy_forms.bootstrap import  FormActions
from django.template.defaultfilters import slugify




# I put this on all required fields, because it's easier to pick up
# on them with CSS or JavaScript if they have a class of "required"
# in the HTML. Your mileage may vary. If/when Django ticket #3515
# lands in trunk, this will no longer be necessary.
attrs_dict = {'class': 'required'}






class RegistrationForm(forms.Form):
    """
    """    
    last_name = forms.RegexField(regex=r'^[a-zA-Z]+$',
                                max_length=20,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Last name"),
                                error_messages={'invalid': _(u"Only caracters are accepted.")})
    first_name = forms.RegexField(regex=r'^[a-zA-Z]+$',
                                max_length=20,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("First name"),
                                error_messages={'invalid': _(u"Only caracters are accepted.")})
    username = forms.RegexField(regex=r'^[a-zA-Z]+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Username"),
                                error_messages={'invalid': _(u"Only caracters are accepted.")})
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_("E-mail"))
    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                min_length = 8,
                                error_messages={'invalid': _(u"Minimum 8 caracters.")},
                                label=_("Password"))
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
                             label=_(u"I agree to the Forum Terms of Service and Privacy Policy."),
                             error_messages={ 'required': _(u"You must accept Forum's Terms of Service and Privacy Policy")})
        
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id_registration'        
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.form_class = "form-horizontal"
        self.helper.error_text_inline = True
        self.helper.layout = Layout(                                                       
            'username',
            'password',
            'email',
            'last_name',
            'first_name',
            'tos',
            FormActions(
                Submit('submit', 'Send', css_class="btn-primary"),
                HTML('<a class="btn" href="/">Cancel</a>')         
                )
            )
        super(RegistrationForm, self).__init__(*args, **kwargs)
        
    def clean_email(self):
        """
        Validate that the supplied email address is unique for the
        site.
        
        """
        if User.objects.filter(email__iexact=self.cleaned_data['email']):
            raise forms.ValidationError(_("This email address is already in use. Please supply a different email address."))
        return self.cleaned_data['email']
    
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

class ThreadForm(forms.Form):
    thread_title = forms.CharField(max_length=40,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Thread title"))
    post_title = forms.CharField(max_length=40,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_("Post Title"))
    post_description =  forms.CharField(max_length=4000,
                                widget=forms.Textarea(attrs=attrs_dict),
                                label=_("Description"))
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = 'id_new_thread'        
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.form_class = "form-horizontal"
        self.helper.error_text_inline = True
        self.helper.layout = Layout(                                                       
            'thread_title',
            'post_title',
            'post_description',
            FormActions(
                Submit('submit', 'Send', css_class="btn-primary"),
                HTML('<a class="btn" href="/">Cancel</a>')         
                )
            )
        super(ThreadForm, self).__init__(*args, **kwargs)
        
    def clean_thread_title(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        """
        existing = Thread.objects.filter(slug__iexact=slugify(self.cleaned_data['thread_title']))
        if existing.exists():
            raise forms.ValidationError(_("Thread already exist."))
        else:
            return self.cleaned_data['thread_title']


class PostForm(forms.Form):
    post_description =  forms.CharField(max_length=4000,
                                widget=forms.Textarea(attrs=attrs_dict),
                                label=_("New Post"))
    def __init__(self, *args, **kwargs):
        self.helper = FormHelper()
        self.helper.form_id = ''        
        self.helper.form_method = 'post'
        self.helper.form_action = '.'
        self.helper.form_class = "form-inline"
        self.helper.error_text_inline = True
        self.helper.layout = Layout('post_description',
                                    FormActions(
                                                Submit('submit', 'Add', css_class="btn-primary")
                )
            )
        super(PostForm, self).__init__(*args, **kwargs)
