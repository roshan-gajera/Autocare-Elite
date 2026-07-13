from django.shortcuts import render, redirect, get_object_or_404
from .forms import registerform
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from portal.models import ServiceOffering, ServiceBooking, TowingRequest, ContactMessage
from portal.forms import ServiceOfferingForm,ServiceBookingForm, TowingRequestForm, ContactMessageForm
from django.contrib import messages
from .models import adminProfile
from .forms import userUpdateForm, profileUpdateForm
from .decorators import staff_required
# Create your views here.


@login_required(login_url='/auth/login/')
@staff_required
def home(request):
    services = ServiceOffering.objects.filter(user = request.user)

    if request.method == 'POST':
        form = userUpdateForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('servicesite-home')
    else:
        form = userUpdateForm(instance=request.user)
    services = {
        'services' : services,
        'form' : form
    }
    return render(request, 'servicesite/index.html',{'services': services})

@login_required(login_url='/auth/login/')
@staff_required
def dashboard(request):
    user_shop = get_object_or_404(adminProfile, user = request.user)
    booking = ServiceBooking.objects.filter(shop=user_shop)
    towing = TowingRequest.objects.filter(shop=user_shop)
    services = {
        'booking' : booking,
        'total_service' : booking.count(),
        'total_towing' : towing.count(),
        'total_customer' : booking.count()+towing.count(),
        'pending_order' : booking.filter(status = "pending").count()+towing.filter(status = "pending").count(),
        'service_customer' : booking.order_by('-id')[:5],
        'towing_customer' : towing.order_by('-id')[:6]
    }
    return render(request, 'servicesite/dashboard.html',{'services': services})


# message page
@login_required(login_url='/auth/login/')
@staff_required
def message(request):
    user_shop = get_object_or_404(adminProfile, user = request.user)
    messages = ContactMessage.objects.filter(shop=user_shop).order_by('-id')
    total_message = messages.count()
    if total_message > 0 :
        read_per = int((ContactMessage.objects.filter(is_read = True).count() * 100)/total_message)
    else:
        read_per = 0
    services = {
        'messages' : messages,
        'total_message' : total_message,
        'read_message' : ContactMessage.objects.filter(is_read = True).count(),
        'not_read_message' : ContactMessage.objects.filter(is_read = False).count(),
        'read_percentage' : read_per
    }
    return render(request, 'servicesite/message.html',{'services': services})

def message_show(request, message_id):
    message = get_object_or_404(ContactMessage, pk = message_id)
    services = {
        'message_show' : message
    }
    return render(request, 'servicesite/message_show.html',{'services':services})


def message_edit(request, message_id):
    message = get_object_or_404(ContactMessage, pk=message_id)
    if request.method == 'POST':
        form = ContactMessageForm(request.POST, instance=message, edit_mode=True)
        if form.is_valid():
            form.save()
            return redirect('servicesite-message')
        
    else:
        form = ContactMessageForm(instance=message, edit_mode=True)
    return render(request,'servicesite/message_edit.html', {'form':form})

# Service Page

@login_required(login_url='/auth/login/')
@staff_required
def serviceorder(request):
    user_shop = get_object_or_404(adminProfile, user = request.user)
    booking = ServiceBooking.objects.filter(shop = user_shop).order_by('-id')

    services ={
        'booking' : booking,
        'total_service' : booking.count(),
        'pending_order' : booking.filter(status = "pending").count(),
        'completed_order' : booking.filter(status = "completed").count(),
        'processing_order' : booking.filter(status = "processing").count(),
        
    }
    return render(request, 'servicesite/services_orders.html', {'services': services})

@login_required(login_url='/auth/login/')
@staff_required
def serviceorder_show(request,order_id):
    order = get_object_or_404(ServiceBooking, pk=order_id)
    services = {
        'order_show' : order
    }
    return render(request, 'servicesite/service_order_show.html', {'services': services})

@login_required(login_url='/auth/login/')
@staff_required
def serviceorder_edit(request, order_id):
    order = get_object_or_404(ServiceBooking, pk=order_id)
    if request.method == 'POST':
        form = ServiceBookingForm(request.POST, instance = order, edit_mode = True, shop = order.shop)
        if form.is_valid():
            form.save()
            return redirect('servicesite-serviceorder')
        else:
            print(form.errors)
    else:
        
        form = ServiceBookingForm(instance=order, edit_mode = True, shop = order.shop)

    return render(request, 'servicesite/service_order_edit.html', {'form':form})


# towing page

@login_required(login_url='/auth/login/')
@staff_required
def towingorder(request):
    user_shop = get_object_or_404(adminProfile, user = request.user)
    towing  = TowingRequest.objects.filter(shop=user_shop).order_by('-id')
    services = {
        'towing' : towing,
        'total_order' : towing.count(),
        'pending_order' : towing.filter(status = "pending").count(),
        'completed_order' : towing.filter(status = "completed").count(),
        'processing_order' : towing.filter(status = "processing").count(),

    }
    return render(request, 'servicesite/towing_orders.html', {'services': services} )

def towing_order_show(request,towing_id):
    towing = get_object_or_404(TowingRequest, pk = towing_id)
    services = {
        'towing_show' : towing
    }
    return render(request, 'servicesite/towing_order_show.html',{'services':services})

def towing_order_edit(request,towing_id):
    towing = get_object_or_404(TowingRequest, pk=towing_id)
    if request.method == 'POST':
        form = TowingRequestForm(request.POST, instance=towing, edit_mode=True)
        if form.is_valid():
            form.save()
            return redirect('servicesite-towingorder')
    else:
        form = TowingRequestForm(instance=towing, edit_mode=True)
    return render(request,'servicesite/towing_order_edit.html',{'form':form})


# Profile page

@login_required(login_url='/auth/login/')
@staff_required
def profile(request):
    serviceOffer = ServiceOffering.objects.filter(user = request.user)
    select_service = None

    profile_obj, created = adminProfile.objects.get_or_create(user=request.user)


    if request.method == "POST":
        form_type = request.POST.get('form_type')

        if form_type == 'select_service':
            select_id = request.POST.get("service_id")
            if select_id :
                select_service = get_object_or_404(ServiceOffering, id = select_id)

            p_form = profileUpdateForm(instance=profile_obj)
        elif form_type == 'adminProfile':
            p_form = profileUpdateForm(request.POST,instance=profile_obj)
            if p_form.is_valid():
                p_user = p_form.save(commit=False)
                p_user.user = request.user
                p_user.save()   
            else:
                return redirect('servicesite-profile')     
    else:
        p_form = profileUpdateForm(instance=profile_obj)

    services = {
        'serviceOffer' : serviceOffer,
        'select_service' : select_service,
        'p_form' : p_form,
    }
    return render(request, 'servicesite/profile.html', {'services': services})

@login_required(login_url='/auth/login/')
@staff_required
def service_add(request):
    if request.method == 'POST':
        form = ServiceOfferingForm(request.POST)
        if form.is_valid():
            shop_user = form.save(commit=False)
            shop_user.user = request.user 
            shop = adminProfile.objects.get(user = request.user)
            shop_user.shop = shop
            shop_user.save()
            messages.success(request, 'Service offering added successfully!')
            return redirect('servicesite-profile')
    else:
        form = ServiceOfferingForm()
    return render(request, 'servicesite/service_add.html', {'form': form})


@login_required(login_url='/auth/login/')
@staff_required
def service_edit(request, service_id):
    service = get_object_or_404(ServiceOffering, pk=service_id)
    if service:
        if request.method == 'POST':
            form = ServiceOfferingForm(request.POST, instance=service)
            if form.is_valid():
                form.save()
                messages.success(request, 'Service offering updated successfully!')
                return redirect('servicesite-profile')
        else:
            form = ServiceOfferingForm(instance=service)
    else:
        return redirect('servicesite-profile')
    return render(request, 'servicesite/service_edit.html', {'form': form})

@login_required(login_url='/auth/login/')
@staff_required
def service_delete(request, service_id):
    service = get_object_or_404(ServiceOffering, pk=service_id)
    if request.method == 'POST':
        service.delete()
        messages.success(request, 'Service offering deleted successfully!')
        return redirect('servicesite-profile')
    return render(request, 'servicesite/service_delete.html', {'object': service})


@login_required
@staff_required
def logout_view(request):
    logout(request)
    return redirect('login')