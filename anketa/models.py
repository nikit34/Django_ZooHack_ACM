from django.db import models
from django.urls import reverse
import uuid
from datetime import date
from django.contrib.auth.models import User


class Claim(models.Model):
    question = models.CharField(max_length=2000, blank=True)
    witness = models.ForeignKey('Witness', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=200, blank=True)
    char_1 = models.CharField(max_length=200, blank=True)
    char_2 = models.CharField(max_length=200, blank=True)
    boolean_1 = models.BooleanField()
    boolean_2 = models.BooleanField()
    boolean_3 = models.BooleanField()
    boolean_4 = models.BooleanField()
    boolean_5 = models.BooleanField()
    boolean_6 = models.BooleanField()
    boolean_7 = models.BooleanField()
    integer_1 = models.IntegerField(blank=True, null=True)
    integer_2 = models.IntegerField(blank=True, null=True)
    image_1 = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    image_2 = models.ImageField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)
    file_1 = models.FileField(upload_to='uploads/%Y/%m/%d/', blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('claim-detail', args=[str(self.id)])


class Status(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular claim across whole reestry')
    claim = models.ForeignKey('Claim', on_delete=models.SET_NULL, null=True)
    LOAN_STATUS = (
        ('i', 'init'),
        ('s', 'sent'),
        ('e', 'editional'),
        ('p', 'prepared'),
        ('d', 'delivered'),
    )
    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='i')
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property
    def is_overdue(self):
        if self.status == 'i' or self.status == 's' or self.status == 'e':
            return True
        return False

    class Meta:
        ordering = ['status']

    def __str__(self):
        return '%s (%s)' % (self.id, self.claim.title)


class Witness(models.Model):
    first_name = models.CharField(max_length=20, help_text='Enter first name')
    second_name = models.CharField(max_length=20, help_text='Enter second name')
    telephon = models.CharField(max_length=10, help_text='Enter telephones number')
    email = models.CharField(max_length=20, help_text='Enter email adderess')
    second_name = models.CharField(max_length=20)
    date_order = models.DateField(null=True, blank=True)
    date_incident = models.DateTimeField('Incident', null=True, blank=True)

    def __str__(self):
        return '%s, %s' % (self.second_name, self.date_order)

    def get_absolute_url(self):
        return reverse('witness-detail', args=[str(self.id)])

    class Meta:
        ordering = ['second_name']


class Post(models.Model):
    title = models.TextField()
    cover = models.ImageField(upload_to='images/')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('index')
