from django.contrib.auth.models import User
from django.db import models


class Schema(models.Model):
    CHARACTERS_CHOICES = (
        ('"', 'Double-quote (")'),
        (';', 'Semicolon (;)'),
        (':', 'Colon (:)'),
        ('^', 'Caret (^)'),
        ('~', 'Tilde (~)'),
    )
    SEPARATOR_CHOICES = (
        (',', 'Comma (,)'),
        (';', 'Semicolon (;)'),
        ('\t', 'Tab (\\t)'),
        ('|', 'Pipe (|)'),
    )

    name = models.CharField(max_length=100)
    data = models.DateField(auto_now=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    column_separator = models.CharField(
        max_length=2,
        choices=SEPARATOR_CHOICES,
        default=',',
        help_text='Select the character used to separate columns in CSV files.',

    )
    column_characters = models.CharField(
        max_length=1,
        choices=CHARACTERS_CHOICES,
        default='"',
        help_text='Select the character used to separate strings in CSV files.',
    )
    # column = models.ForeignKey('authentication.Column',
    #                            on_delete=models.CASCADE,
    #                            related_name='schemas')


class Column(models.Model):
    TYPE_CHOICES = [
        ('full_name', 'Full Name'),
        ('job', 'Job'),
        ('email', 'Email'),
        ('domain_name', 'Domain Name'),
        ('phone_number', 'Phone Number'),
        ('company_name', 'Company Name'),
        ('text', 'Text'),
        ('integer', 'Integer'),
        ('address', 'Address'),
        ('date', 'Date'),
    ]

    name = models.CharField(max_length=100)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE)
    type = models.CharField(max_length=100, choices=TYPE_CHOICES)
    range_start = models.IntegerField(null=True, blank=True)
    range_end = models.IntegerField(null=True, blank=True)
    order = models.IntegerField()


class DataSet(models.Model):
    name = models.CharField(max_length=100)
    data = models.DateField(auto_now=True)
    csv = models.FileField(upload_to='csv/')
    status = models.BooleanField(default=False)
    schema = models.ForeignKey(Schema, on_delete=models.CASCADE,
                               related_name='dataset')
