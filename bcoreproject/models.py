import datetime
from django.conf import settings
from django.db import models
from rest_framework.reverse import reverse
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class RiskType(models.Model):
	User = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	Title  = models.CharField(max_length=30)

	def get_uri(self, request=None):
		return reverse('api-risktypes:risktype-rud', kwargs={'pk': self.pk}, request=request)

	def __str__(self):
		return 'Title: {}'.format(self.Title)

	@property
	def owner(self):
		return self.User

class RiskTypeGenericType(models.Model):
	RiskType = models.ForeignKey(
		RiskType,
		related_name='RiskTypeGenericType',
		on_delete=models.CASCADE
	)
	TEXT = '1'
	NUMBER = '2'
	DATE = '3'
	ENUM = '4'
	FIELD_TYPE_CHOICES = (
		(TEXT, 'text'),
		(NUMBER, 'number'),
		(DATE, 'date'),
		(ENUM, 'enum'),
	)
	Type = models.CharField(
		max_length=1,
		choices=FIELD_TYPE_CHOICES,
		default=TEXT,
		null=False
	)
	FieldTitle = models.CharField(max_length=32, null=False, blank=False)

	@property
	def FieldValue(self):
		result = RiskTypeGenericTypeValue.objects.filter(RiskTypeGenericType=self).first()
		if result:
			return result.get_generic_type_value()
		return None

	@property
	def TypeAsText(self):
		return self.FIELD_TYPE_CHOICES[int(self.Type)-1][1]

	@property
	def owner(self):
		return self.RiskType.User

	def get_uri(self, request=None):
		return reverse('api-risktypes:risktype-generic-type-ud', kwargs={'pk': self.pk}, request=request)

	def __str__(self):
		return '\n Type: {} \n RiskType: {} \n Value {}'.format(
			self.FIELD_TYPE_CHOICES[int(self.Type)-1][1],
			self.RiskType.Title,
			self.FieldValue
		)

class RiskTypeGenericTypeValue(models.Model):
	RiskTypeGenericType = models.OneToOneField(
		RiskTypeGenericType,
		related_name='RiskTypeGenericTypeValue',
		on_delete=models.CASCADE
	)
	TextValue = models.TextField(null=True, blank=True)
	NumberValue = models.IntegerField(null=True, blank=True)
	DateValue = models.DateField(null=True, blank=True)
	EnumValue = models.TextField(null=True, blank=True)

	def clean(self):
		if not self.pk:
			if self.RiskTypeGenericType.TypeAsText is 'text' and (
				(self.TextValue is None) or
				(type(self.TextValue) is not str) or
				(not self.TextValue)
			):
				raise ValidationError("Illegal value: TextValue is not a string.")

			if self.RiskTypeGenericType.TypeAsText is 'number' and (
				(self.NumberValue is None) or
				(type(self.NumberValue) is not int) or
				(not self.NumberValue)
			):
				raise ValidationError("Illegal value: NumberValue is not a number.")

			if self.RiskTypeGenericType.TypeAsText is 'date' and (
				(self.DateValue is None) or
				(not isinstance(self.DateValue, datetime.date))
			):
				raise ValidationError("Illegal value: DateValue is not a date.")

	def get_generic_type_value(self):
		if self.RiskTypeGenericType.TypeAsText is 'text':
			return self.TextValue
		elif self.RiskTypeGenericType.TypeAsText is 'number':
			return self.NumberValue
		elif self.RiskTypeGenericType.TypeAsText is 'date':
			return self.DateValue
		elif self.RiskTypeGenericType.TypeAsText is 'enum':
			return self.EnumValue

		return None

	@property
	def owner(self):
		return self.RiskTypeGenericType.RiskType.User