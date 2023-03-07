from django import forms
from .models import Schema, Column
from django.contrib.auth.forms import AuthenticationForm


class SchemaForm(forms.ModelForm):

    class Meta:
        model = Schema
        fields = ['name', 'column_separator', 'column_characters']


class ColumnForm(forms.ModelForm):

    class Meta:
        model = Column
        fields = ['name', 'type', 'range_start', 'range_end', 'order']


class MyAuthenticationForm(AuthenticationForm):
    # from django.forms.widgets import PasswordInput
    # password = forms.CharField(
    #     label="Password",
    #     strip=False,
    #     widget=PasswordInput(render_value=True),
    # )
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['value'] = 'Username'
        self.fields['password'].widget.attrs['value'] = 'Password'
