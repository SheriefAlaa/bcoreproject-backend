from django.contrib import admin
from .models import *


admin.site.register(RiskType)
admin.site.register(RiskTypeGenericType)
admin.site.register(RiskTypeGenericTypeValue)