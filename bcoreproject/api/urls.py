from django.conf.urls import url
from .views import RiskTypeAPIView, RiskTypeView, RiskTypeGenericTypeAPIView, RiskTypeGenericTypeView


urlpatterns = [
	# Create, List, and Find RiskType
	url(r'^$', RiskTypeAPIView.as_view(), name='risktype-cls'),
	# Retrieve, Update, and Delete a RiskType
    url(r'^(?P<pk>\d+)/$', RiskTypeView.as_view(), name='risktype-rud'),
    # Create RiskTypeGenericType
	url(r'^generic_type/$', RiskTypeGenericTypeAPIView.as_view(), name='risktype-generic-type-c'),
	url(r'^generic_type/(?P<pk>\d+)/$', RiskTypeGenericTypeView.as_view(), name='risktype-generic-type-ud'),

]
