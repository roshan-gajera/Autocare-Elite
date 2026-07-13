from django.shortcuts import render, redirect
from .decorators import super_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from portal.models import ServiceBooking, TowingRequest, ServiceOffering
from servicesite.models import adminProfile
from django.contrib.auth.models import User
from .forms import providerRegisterForm
from servicesite.models import adminProfile

# Create your views here.

@login_required(login_url='/auth/login/')
@super_required
def home(request):
    all_service = ServiceBooking.objects.all().order_by('-id')
    all_towing = TowingRequest.objects.all().order_by('-id')
    services = {
        'all_service' : all_service[:6],
        'all_towing' : all_towing[:6],
        'total_service':all_service.count(),
        'total_towing':all_towing.count(),
        'total_provider' : adminProfile.objects.all().count(),
        'service_provider': ServiceOffering.objects.all().count(),
        'total_user' : User.objects.filter(is_staff = False).count()
    }
    return render(request, "superadmin/dashboard.html", {'services':services})


@login_required(login_url='/auth/login/')
@super_required
def services(request):
    all_services = ServiceBooking.objects.all().order_by('-id')
    service = {
        'all_service' : all_services
    }
    return render(request, "superadmin/services.html", {'service':service})

@login_required(login_url='/auth/login/')
@super_required
def deleteService(request,pk):
    select_service = ServiceBooking.objects.get(id = pk)
    select_service.delete()
    return redirect('admin-services')

@login_required(login_url='/auth/login/')
@super_required
def deleteTowing(request,pk):
    select_towing = TowingRequest.objects.get(id = pk)
    select_towing.delete()
    return redirect('admin-towing')


@login_required(login_url='/auth/login/')
@super_required
def towing(request):
    all_towing = TowingRequest.objects.all().order_by('-id')
    towing = {
        'all_towing':all_towing
    }
    return render(request, "superadmin/towing.html", {'towing':towing})


@login_required(login_url='/auth/login/')
@super_required
def addProvider(request):
    if request.method == "POST":
        form=  providerRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form=  providerRegisterForm()
    return render(request, "superadmin/add-provider.html", {'form':form})


@login_required(login_url='/auth/login/')
@super_required
def providers(request):
    all_provider = adminProfile.objects.all()
    provider = {
        'all_provider' : all_provider
    }
    return render(request, "superadmin/providers.html", {'provider':provider})

@login_required(login_url='/auth/login/')
@super_required
def deleteProvider(request,pk):
    select_provider = User.objects.get(id = pk)
    select_provider.delete()
    return redirect("admin-providers")

@login_required(login_url='/auth/login/')
@super_required
def logout_view(request):
    logout(request)
    return redirect("login")

