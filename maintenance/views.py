from django.shortcuts import render, get_object_or_404, redirect
from .forms import userUpdateForm, selectShopForm
from servicesite.models import adminProfile
from .models import selectShop
from portal.models import ServiceBooking,TowingRequest,ContactMessage

from portal.decorators import user_required

@user_required
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')

@user_required
def dashboard(request):
    service_order = ServiceBooking.objects.filter(user = request.user)
    towing_order = TowingRequest.objects.filter(user = request.user)
    message_show = ContactMessage.objects.filter(user = request.user)
    
    services= {
        'total_order' : service_order.count()+towing_order.count(),
        'service_order' : service_order.order_by('-id')[:3],
        'towing_order' : towing_order.order_by('-id')[:3],
        'total_service_order': service_order.count() ,
        'active_service_order':service_order.filter(status = 'processing').count(),
        'total_towing_order' : towing_order.count(),
        'active_towing_order' : towing_order.filter(status = 'processing').count(),
        
    }
    return render(request, 'maintenance/dashboard.html', {'services':services})

# Car CRUD
@user_required
def serviceorder(request):
    services_order = ServiceBooking.objects.filter(user = request.user)
    services = {
        'service_order' : services_order.order_by('-id'),
        'pending_order' : services_order.filter(status = 'pending').count(),
        'confirmed_order' : services_order.filter(status = 'confirmed').count(),
        'processing_order' : services_order.filter(status = 'processing').count(),
        'completed_order' : services_order.filter(status = 'completed').count(),
        'cancelled_order' : services_order.filter(status = 'cancelled').count(),
    }
    return render(request, 'maintenance/service_orders.html', {'services': services})

@user_required
def towingorder(request):
    towing_order = TowingRequest.objects.filter(user = request.user)
    services = {
        'towing_order' : towing_order.order_by('-id'),
        'pending_order' : towing_order.filter(status = 'pending').count(),
        'processing_order' : towing_order.filter(status = 'processing').count(),
        'completed_order' : towing_order.filter(status = 'completed').count(),
        'cancelled_order' : towing_order.filter(status = 'cancelled').count(),
    }
    return render(request, 'maintenance/towing_orders.html', {'services':services})


@user_required
def profile(request):
    shop_obj, created = selectShop.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        # Update user profile
        if form_type == "profile":
            u_form = userUpdateForm(request.POST, instance=request.user)
            s_form = selectShopForm(instance=shop_obj)

            if u_form.is_valid():
                u_form.save()
                return redirect("user_profile")

        # Update selected shop
        elif form_type == "select_shop":
            u_form = userUpdateForm(instance=request.user)
            s_form = selectShopForm(request.POST, instance=shop_obj)

            if s_form.is_valid():
                s_form.save()
                return redirect("user_profile")

    else:
        u_form = userUpdateForm(instance=request.user)
        s_form = selectShopForm(instance=shop_obj)

    context = {
        'u_form': u_form,
        's_form': s_form,
        'shop': adminProfile.objects.all(),
    }

    return render(request, 'maintenance/profile.html', {'services': context})