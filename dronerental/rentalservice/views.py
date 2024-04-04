from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status

from dronerental.rentalservice.models import Category, Brand, UAV, RentalTransaction
from dronerental.rentalservice.serializers import GroupSerializer, UserSerializer, CategorySerializer, BrandSerializer, \
    UAVSerializer, RentalTransactionSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class UAVViewSet(viewsets.ModelViewSet):
    queryset = UAV.objects.all()
    serializer_class = UAVSerializer


class RentalTransactionListCreate(APIView):
    def get(self, request, format=None):
        rentals = RentalTransaction.objects.all()
        serializer = RentalTransactionSerializer(rentals, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = RentalTransactionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RentalTransactionDetail(APIView):
    def get_object(self, pk):
        try:
            return RentalTransaction.objects.get(pk=pk)
        except RentalTransaction.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        rental = self.get_object(pk)
        serializer = RentalTransactionSerializer(rental)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        rental = self.get_object(pk)
        serializer = RentalTransactionSerializer(rental, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        rental = self.get_object(pk)
        rental.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
