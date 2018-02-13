from django.contrib.auth import get_user_model
from datetime import date


from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from rest_framework_jwt.settings import api_settings

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler  = api_settings.JWT_ENCODE_HANDLER

from bcoreproject.models import RiskType, \
	 RiskTypeGenericType, \
	 RiskTypeGenericTypeValue

User = get_user_model()

class RiskTypeTestCase(APITestCase):
	def setUp(self):
		user = User(username='test_api_user')
		user.set_password('test_api_password')
		user.save()
		risk_type_obj = RiskType.objects.create(
			User=user,
			Title='Prize'
		)
		risk_type_generic_type = RiskTypeGenericType.objects.create(
			RiskType=risk_type_obj,
			Type='1',
			FieldTitle='TestTitle'
		)
		RiskTypeGenericTypeValue.objects.create(
			RiskTypeGenericType=risk_type_generic_type,
			TextValue="Some Test Text"
		)

	def test_single_user(self):
		user_count = User.objects.count()
		self.assertEqual(user_count, 1)

	def test_single_risk_type(self):
		risk_type_count = RiskType.objects.count()
		self.assertEqual(risk_type_count, 1)

	# Create
	def test_post_risk_type(self):
		user = User.objects.first()
		data = {
			"User": user.pk,
			"Title": "Some Title"
		}
		uri = reverse("api-risktypes:risktype-cls")
		payload  = payload_handler(user)
		token_response = encode_handler(payload)
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response)
		response = self.client.post(uri, data, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	# Create RiskTypeGenericType
	def test_post_risk_type_generic_type_text_value_without_user(self):
		data = {
			"RiskType": RiskType.objects.first().pk,
			"Type": "1",
			"FieldTitle": "String without user genericType",
			"FieldValue": "Some Text"
		}
		uri = reverse("api-risktypes:risktype-generic-type-c")
		response = self.client.post(uri, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
		response = self.client.get(uri, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

	def test_post_risk_type_generic_type_text_value(self):
		data = {
			"RiskType": RiskType.objects.first().pk,
			"Type": "1",
			"FieldTitle": "Some field with a string",
			"FieldValue": "Some Text"
		}
		uri = reverse("api-risktypes:risktype-generic-type-c")
		user = User.objects.first()
		payload  = payload_handler(user)
		token_response = encode_handler(payload)
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response)
		response = self.client.post(uri, data, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_post_risk_type_generic_type_number_value(self):
		data = {
			"RiskType": RiskType.objects.first().pk,
			"Type": "2",
			"FieldTitle": "Some field with a number",
			"FieldValue": int(13),
		}
		uri = reverse("api-risktypes:risktype-generic-type-c")
		user = User.objects.first()
		payload  = payload_handler(user)
		token_response = encode_handler(payload)
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response)
		response = self.client.post(uri, data, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_post_risk_type_generic_type_date_value(self):
		data = {
			"RiskType": RiskType.objects.first().pk,
			"Type": "3",
			"FieldTitle": "Some field with a number",
			"FieldValue": date.today(),
		}
		uri = reverse("api-risktypes:risktype-generic-type-c")
		user = User.objects.first()
		payload  = payload_handler(user)
		token_response = encode_handler(payload)
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response)
		response = self.client.post(uri, data, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_post_risk_type_generic_type_enum_value(self):
		data = {
			"RiskType": RiskType.objects.first().pk,
			"Type": "4",
			"FieldTitle": "Some field with a number",
			"FieldValue": "Type1, Type2.., Type3   ",
		}
		uri = reverse("api-risktypes:risktype-generic-type-c")
		user = User.objects.first()
		payload  = payload_handler(user)
		token_response = encode_handler(payload)
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response)
		response = self.client.post(uri, data, format="json")
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	# Retrieve single RiskType
	def test_get_risk_type(self):
		data = {}
		uri = RiskType.objects.first().get_uri()
		user = User.objects.first()
		payload  = payload_handler(user)
		token_response = encode_handler(payload)
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response)
		response = self.client.get(uri, data, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	# Update
	def test_update_generic_type_without_user(self):
		risk_type_generic_type = RiskTypeGenericType.objects.first()
		data = {
			'FieldTitle': 'TestTitleChanged!'
		}
		uri = risk_type_generic_type.get_uri()
		response = self.client.post(uri, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
		response = self.client.put(uri, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

	def test_update_generic_type_with_auth(self):
		data = {
			"RiskType": RiskType.objects.first().pk,
			"Type": "1",
			"FieldTitle": "Some field with a string",
			"FieldValue": "Some Text2"
		}
		uri = RiskTypeGenericType.objects.first().get_uri()
		user = User.objects.first()
		payload  = payload_handler(user)
		token_rsp = encode_handler(payload)
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_rsp)
		response = self.client.put(uri, data, format='json')
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	# List (all RiskTypes for user)
	def test_get_risk_types_list(self):
		data = {}
		uri = reverse("api-risktypes:risktype-cls")
		user = User.objects.first()
		payload  = payload_handler(user)
		token_response = encode_handler(payload)
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response)
		response = self.client.get(uri, data, format="json")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	# Find
	def test_find_risk_type(self):
		data = {"q": "Prize"}
		uri = reverse("api-risktypes:risktype-cls")
		user = User.objects.first()
		payload  = payload_handler(user)
		token_response = encode_handler(payload)
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response)
		response = self.client.get(uri, data, format="json")
		title = list(response.data[0].items())[2][1]
		self.assertEqual(title, data['q'])

	# Delete
	def test_delete_risk_type(self):
		data = {}
		uri = RiskType.objects.first().get_uri()
		user = User.objects.first()
		payload  = payload_handler(user)
		token_response = encode_handler(payload)
		self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token_response)
		response = self.client.delete(uri, data, format="json")
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)