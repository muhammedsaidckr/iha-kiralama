from django.contrib.auth.models import Group, User
from rest_framework import permissions, viewsets, filters, status
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.response import Response
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from django.db.models import Q

from dronerental.rentalservice.forms import SignUpForm, RentalForm
from dronerental.rentalservice.models import Category, Brand, UAV, RentalTransaction
from dronerental.rentalservice.serializers import GroupSerializer, UserSerializer, CategorySerializer, BrandSerializer, \
    UAVSerializer, RentalTransactionSerializer


def index(request):
    return render(request, 'dronerental/rentalservice/welcome.html')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect(
                'index')  # Burada kullanıcıyı anasayfaya yönlendiriyoruz. 'home' url adınız neyse onu kullanın.
    else:
        form = SignUpForm()
    return render(request, 'dronerental/rentalservice/signup.html', {'form': form})


@login_required
def user_dashboard(request):
    return render(request, 'dronerental/rentalservice/admin/dashboard.html')

@login_required
def rental_list(request):
    return render(request, 'dronerental/rentalservice/admin/rental_list.html')

@login_required
def list_uavs(request):
    return render(request, 'dronerental/rentalservice/admin/list_uavs.html')

@login_required
def get_rent_uav(request, uav_id):
    uav = get_object_or_404(UAV, id=uav_id)
    form = RentalForm()

    return render(request, 'dronerental/rentalservice/admin/rent_uav.html', {'form': form, 'uav': uav})

def logout_view(request):
    logout(request)
    return redirect('index')

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
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']


class RentalTransactionViewSet(viewsets.ModelViewSet):
    queryset = RentalTransaction.objects.all()
    serializer_class = RentalTransactionSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['uav__name', 'user__username']

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class RentalTransactionsListAPIView(APIView):
    def get(self, request, format=None):
        search_value = request.GET.get('search[value]', None)

        # Önce filtreleme yap
        query = RentalTransaction.objects.all()

        if search_value:
            query = query.filter(
                Q(uav__name__icontains=search_value) |
                Q(user__username__icontains=search_value) |
                Q(start_date__icontains=search_value) |
                Q(end_date__icontains=search_value)
            )
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        total_records = query.count()  # Filtreleme yapıldıktan sonra toplam kayıt sayısını al
        records_filtered = query.count()  # Filtrelenmiş kayıt sayısı

        # Sonra dilimleme yap
        query = query[start:start + length]

        serializer = RentalTransactionSerializer(query, many=True)

        # DataTables tarafından beklenen response yapısını oluştur
        data = {
            "draw": int(request.GET.get('draw', 1)),
            "recordsTotal": total_records,
            "recordsFiltered": records_filtered,
            "data": serializer.data
        }

        return Response(data)


class UAVListAPIView(APIView):
    def get(self, request, format=None):
        search_value = request.GET.get('search[value]', None)

        # Önce filtreleme yap
        query = UAV.objects.all()

        if search_value:
            query = query.filter(
                Q(name__icontains=search_value)
            )

        order_column = request.GET.get('order[0][column]')
        order_direction = request.GET.get('order[0][dir]')

        # Sıralama işlemi için sütun adlarını bir listeye eşle
        order_fields = ['id', 'name', 'description', 'category__name', 'brand__name', 'hourly_rate']
        if order_column:
            order_field = order_fields[int(order_column)]
            if order_direction == 'desc':
                order_field = '-' + order_field
            query = query.order_by(order_field)

        total_records = query.count()  # Filtreleme ve sıralama yapıldıktan sonra toplam kayıt sayısını al
        records_filtered = total_records  # Bu örnekte, records_filtered ve total_records aynı
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 10))
        # Sonra dilimleme yap
        query = query[start:start + length]

        serializer = UAVSerializer(query, many=True)

        # DataTables tarafından beklenen response yapısını oluştur
        data = {
            "draw": int(request.GET.get('draw', 1)),
            "recordsTotal": total_records,
            "recordsFiltered": records_filtered,
            "data": serializer.data
        }

        return Response(data)

class RentUAVView(APIView):
    def post(self, request, uav_id):
        uav = get_object_or_404(UAV, id=uav_id)
        form = RentalForm(request.POST)
        if form.is_valid():
            # Formdan alınan bilgilerle kiralama işlemi oluştur
            RentalTransaction.objects.create(
                uav=uav,
                user=request.user,  # Oturum açmış kullanıcı
                start_date=form.cleaned_data['start_date'],
                end_date=form.cleaned_data['end_date'],
                # total_cost hesaplaması gerekirse burada yapılabilir
            )
            return Response({'message': 'UAV kiralama işlemi başarılı'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': form.errors}, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginView(LoginView):
    def form_valid(self, form):
        """Superuser'ları admin paneline, diğer kullanıcıları dashboard'a yönlendir."""
        login(self.request, form.get_user())
        if self.request.user.is_superuser:
            return redirect('/admin/')
        else:
            return redirect('user_dashboard')
