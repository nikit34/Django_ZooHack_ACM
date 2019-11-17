from django import forms
from .models import Post
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
import datetime

class RenewClaimForm(forms.Form):
    renewal_date = forms.DateField(help_text="Enter a date between now and 4 weeks (default 3).")

    def clean_renewal_date(self):
        data = self.cleaned_data['renewal_date']
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - renewal in past'))
        if data > datetime.date.today() + datetime.timedelta(weeks=4):
            raise ValidationError(_('Invalid date - renewal more than 4 weeks ahead'))
        return data

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'cover']
