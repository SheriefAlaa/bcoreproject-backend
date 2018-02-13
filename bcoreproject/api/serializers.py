from collections import OrderedDict
from datetime import datetime

from rest_framework import serializers

from bcoreproject.models import RiskType, RiskTypeGenericType, RiskTypeGenericTypeValue


class RiskTypeGenericTypeSerializer(serializers.ModelSerializer):
	FieldValue = serializers.SerializerMethodField('get_FieldValue')
	class Meta:
		model = RiskTypeGenericType
		fields = [
			'pk',
			'RiskType',
			'Type',
			'TypeAsText',
			'FieldTitle',
			'FieldValue'
		]

	def FieldValue(self, obj):
		return obj.FieldValue

	def create(self, validated_data):
		risk_type_generic_type_obj = super(
			RiskTypeGenericTypeSerializer,
			self
		).create(validated_data)
		request = self.context.get("request")
		FieldValue = request.data['FieldValue']

		if risk_type_generic_type_obj:
			risktype_type = risk_type_generic_type_obj.TypeAsText
			if risktype_type is 'text':
				RiskTypeGenericTypeValue.objects.create(
					RiskTypeGenericType=risk_type_generic_type_obj,
					TextValue=FieldValue
				)
			elif risktype_type is 'number':
				RiskTypeGenericTypeValue.objects.create(
					RiskTypeGenericType=risk_type_generic_type_obj,
					NumberValue=FieldValue
				)
			elif risktype_type is 'date':
				RiskTypeGenericTypeValue.objects.create(
					RiskTypeGenericType=risk_type_generic_type_obj,
					DateValue=FieldValue
				)
			elif risktype_type is 'enum':
				RiskTypeGenericTypeValue.objects.create(
					RiskTypeGenericType=risk_type_generic_type_obj,
					EnumValue=FieldValue
				)
		else:
			raise serializers.ValidationError("Could not create a RiskTypeGenericType.")

		risk_type_generic_type_obj.save()
		return risk_type_generic_type_obj

	def get_uri(self, RiskTypeGenericType):
		request = self.context.get("request")
		return RiskTypeGenericType.get_uri(request=request)

class RiskTypeSerializer(serializers.ModelSerializer):
	RiskTypeGenericType = RiskTypeGenericTypeSerializer(many=True, read_only=True)
	uri = serializers.SerializerMethodField(read_only=True)
	class Meta:
		model = RiskType
		fields = [
			'uri',
			'User',
			'Title',
			'RiskTypeGenericType'
		]
		read_only_fields = ['User']

	def validate_Title(self, value):
		result = RiskType.objects.filter(Title__iexact=value)
		if self.instance:
			result = result.exclude(pk=self.instance.pk)
		if result.exists():
			raise serializers.ValidationError("The title was used in a different RiskType, please use another.")
		return value

	def get_uri(self, RiskType):
		request = self.context.get("request")
		return RiskType.get_uri(request=request)
