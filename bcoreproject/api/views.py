from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from bcoreproject.models import *
from .serializers import RiskTypeSerializer, RiskTypeGenericTypeSerializer
from .permissions import IsOwnerOrReadOnly


class RiskTypeAPIView(mixins.CreateModelMixin, generics.ListAPIView):
	lookup_field = 'pk'
	serializer_class = RiskTypeSerializer
	permission_classes      = [IsAuthenticatedOrReadOnly]

	def get_queryset(self):
		result = RiskType.objects.all()
		query = self.request.GET.get("q")

		if query is not None:
			result = result.filter(Title__icontains=query) \
							.filter(User=self.request.user.pk) \
							.distinct()
		return result

	def perform_create(self, serializer):
		serializer.save(User=self.request.user)

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)


class RiskTypeView(generics.RetrieveUpdateDestroyAPIView):
	lookup_field = 'pk'
	queryset = RiskType.objects.all()
	serializer_class = RiskTypeSerializer
	permission_classes      = [IsOwnerOrReadOnly]

	def get_serializer_context(self, *arge, **kwargs):
		return {"request": self.request}

class RiskTypeGenericTypeAPIView(generics.CreateAPIView):
	queryset = RiskTypeGenericType.objects.all()
	serializer_class = RiskTypeGenericTypeSerializer
	permission_classes      = [IsAuthenticatedOrReadOnly]

	def get_serializer_context(self, *arge, **kwargs):
		return {"request": self.request}

	def post(self, request, *args, **kwargs):
		return self.create(request, *args, **kwargs)


class RiskTypeGenericTypeView(generics.UpdateAPIView, generics.DestroyAPIView):
	queryset = RiskTypeGenericType.objects.all()
	serializer_class = RiskTypeGenericTypeSerializer
	permission_classes      = [IsOwnerOrReadOnly]

	def get_serializer_context(self, *arge, **kwargs):
		return {"request": self.request}

	def put(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def patch(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)

	def delete(self, request, *args, **kwargs):
		return self.update(request, *args, **kwargs)
