from django.shortcuts import render, redirect, get_object_or_404
from .models import ServiceOffering, BlogPost, ContactMessage, TowingRequest, ServiceBooking
from .forms import ServiceOfferingForm, BlogPostForm, ContactMessageForm, TowingRequestForm, ServiceBookingForm
from django.contrib import messages
from django.db.models import Q
import stripe
from django.conf import settings

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from maintenance.models import selectShop
from servicesite.models import adminProfile
from .decorators import user_required


def about_us(request):
    return render(request, 'portal/about_us.html')

@user_required
def service_list(request):
    select = selectShop.objects.get(user = request.user).select_shop
    services = ServiceOffering.objects.filter(shop = select, is_active = True)
    return render(request, 'portal/service_list.html', {'services': services})


def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'portal/blog_list.html', {'posts': posts})


@login_required(login_url='login')
@user_required
def blog_add(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.user = request.user
            blog.save()
           
            return redirect('blog_list')
    else:
        form = BlogPostForm()
    return render(request, 'portal/form.html', {'form': form, 'title': 'Add Blog Post'})

@login_required(login_url='login')
@user_required
def blog_edit(request, blog_id):
    post = get_object_or_404(BlogPost, pk=blog_id)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
           
            return redirect('blog_list')
    else:
        form = BlogPostForm(instance=post)
    return render(request, 'portal/form.html', {'form': form, 'title': 'Edit Blog Post'})

@login_required(login_url='login')
@user_required
def blog_delete(request, blog_id):
    post = get_object_or_404(BlogPost, pk=blog_id)
    if request.method == 'POST':
        post.delete()
        
        return redirect('blog_list')
    return render(request, 'portal/confirm_delete.html', {'object': post, 'type': 'Blog Post'})


@login_required(login_url='login')
@user_required
def contact_us(request):
    select = selectShop.objects.get(user = request.user).select_shop
    select_shop = str(select).split("=")[0].strip()
    try:
        select_info = adminProfile.objects.get(shop_name = select_shop)
    except adminProfile.DoesNotExist:
        select_info = None
    
    if request.method == 'POST':
        form = ContactMessageForm(request.POST)
        if form.is_valid():
            contect = form.save(commit=False)
            contect.user = request.user
            contect.shop = select
            contect.save()
            
            return render(request, 'portal/contact_success.html')
    else:
        form = ContactMessageForm()

    services = {
        'form':form,
        'select_info':select_info
    }
    return render(request, 'portal/contact_us.html', {'services': services})




# ============ SERVICE BOOKING CRUD ============

@login_required(login_url='login')
@user_required
def booking_detail(request, booking_id):
    """View details of a specific booking"""
    booking = get_object_or_404(ServiceBooking, pk=booking_id)
    return render(request, 'portal/booking_detail.html', {'booking': booking})

@login_required(login_url='login')
@user_required
def booking_edit(request, booking_id):
    """Edit an existing service booking"""
    booking = get_object_or_404(ServiceBooking, pk=booking_id)
    
    # Only allow editing if not completed or cancelled
    if booking.status in ['completed', 'cancelled']:
        
        return redirect('booking_detail', booking_id=booking.id)
    
    if request.method == 'POST':
        form = ServiceBookingForm(request.POST, instance=booking, shop = booking.shop)
        if form.is_valid():
            form.save()
            
            return redirect('booking_detail', booking_id=booking.id)
    else:
        form = ServiceBookingForm(instance=booking, shop = booking.shop)
    
    return render(request, 'portal/booking_form.html', {'form': form, 'booking': booking, 'title': 'Edit Booking'})

@login_required(login_url='login')
@user_required
def booking_delete(request, booking_id):
    """Delete/Cancel a service booking"""
    booking = get_object_or_404(ServiceBooking, pk=booking_id)
    
    if request.method == 'POST':
        booking.status = 'cancelled'
        booking.save()
       
        return redirect('dashboard')
    
    return render(request, 'portal/confirm_delete.html', {'object': booking, 'type': 'Service Booking'})

@login_required(login_url='login')
@user_required
def book_service(request, service_id):
    """Create a new service booking"""
    service = get_object_or_404(ServiceOffering, pk=service_id)
    selected_shop = selectShop.objects.get(user=request.user).select_shop
    if request.method == 'POST':
        form = ServiceBookingForm(request.POST, shop= selected_shop)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.shop = selectShop.objects.get(user=request.user).select_shop
            booking.save()

            form.save_m2m()
            
            amount = int(booking.total_estimated_cost() * 100) # Stripe uses cents/paise
            if amount > 0 and booking.payment_method == 'online':
                try:
                    stripe.api_key = settings.STRIPE_SECRET_KEY
                    intent = stripe.PaymentIntent.create(
                        amount=amount,
                        currency='inr',
                        description=f"AutoFix Booking ID: {booking.id}",
                        receipt_email=booking.customer_email
                    )
                    
                    # Store the intent ID to track the payment later
                    booking.stripe_payment_intent_id = intent['id']
                    booking.save()
                    
                    return render(request, 'portal/payment_checkout_stripe.html', {
                        'booking': booking,
                        'client_secret': intent['client_secret'],
                        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
                        'amount_display': booking.total_estimated_cost()
                    })
                except Exception as e:
                    # Graceful fallback if Stripe API keys are incorrect/mocked
                    otp = booking.generate_otp()
                
                    messages.warning(request, 'Test Mode: Payment Gateway is currently disabled or has invalid API keys. Your booking has been generated without upfront payment.')
                    return render(request, 'portal/booking_success.html', {'booking': booking, 'otp': otp})
            else:
                otp = booking.generate_otp()
                return render(request, 'portal/booking_success.html', {'booking': booking, 'otp': otp})
    else:
        form = ServiceBookingForm(initial={'services': [service]}, shop= selected_shop)
    return render(request, 'portal/book_service.html', {'form': form, 'service': service})

@login_required(login_url='login')
@user_required
def pay_online(request, booking_id):
    """Pay an existing unplugged booking bill online using Stripe"""
    booking = get_object_or_404(ServiceBooking, pk=booking_id)
    
    amount = int(booking.total_estimated_cost() * 100) # Stripe uses cents/paise
    
    if booking.is_paid:
        # messages.info(request, "This booking has already been paid.")
        return redirect('booking_detail', booking_id=booking.id)
        
    try:
        stripe.api_key = settings.STRIPE_SECRET_KEY
        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='inr',
            description=f"AutoFix Bill Payment ID: {booking.id}",
            receipt_email=booking.customer_email
        )
        
        # Track the payment intent ID
        booking.stripe_payment_intent_id = intent['id']
        booking.save()
        
        return render(request, 'portal/payment_checkout_stripe.html', {
            'booking': booking,
            'client_secret': intent['client_secret'],
            'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
            'amount_display': booking.total_estimated_cost()
        })
    except Exception as e:
        # messages.error(request, f"Payment system error: {str(e)}")
        return redirect('booking_detail', booking_id=booking.id)

@login_required(login_url='login')
@user_required
@csrf_exempt
def payment_verify(request):
    """Verify Stripe payment and send WhatsApp confirmation"""
    if request.method == "POST":
        data = request.POST
        payment_intent_id = data.get('payment_intent_id')
        
        booking = get_object_or_404(ServiceBooking, stripe_payment_intent_id=payment_intent_id)
        
        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            if intent.status == 'succeeded':
                booking.is_paid = True
                booking.save()
                
                otp = booking.generate_otp()
                
                return render(request, 'portal/booking_success.html', {'booking': booking, 'otp': otp})
            else:
                # messages.error(request, 'Payment Verification Failed: Payment was not successful.')
                return redirect('client_dashboard')
                
        except Exception as e:
            # messages.error(request, f'Payment Verification Error: {str(e)}')
            return redirect('client_dashboard')
            
    return redirect('client_dashboard')

# ============ TOWING REQUEST CRUD ============

@login_required(login_url='login')
@user_required
def towing_detail(request, towing_id):
    """View details of a specific towing request"""
    towing = get_object_or_404(TowingRequest, pk=towing_id)
    return render(request, 'portal/towing_detail.html', {'towing': towing})

@login_required(login_url='login')
@user_required
def towing_request(request):
    """Create a new towing request"""
    if request.method == 'POST':
        form = TowingRequestForm(request.POST)
        if form.is_valid():
            towing = form.save(commit=False)
            towing.user = request.user
            towing.shop = selectShop.objects.get(user=request.user).select_shop
            towing.save()
            otp = towing.generate_otp()
    
            return render(request, 'portal/towing_success.html', {'otp': otp, 'phone': towing.phone_number, 'towing': towing})
    else:
        form = TowingRequestForm()
    return render(request, 'portal/towing_request.html', {'form': form})

@login_required(login_url='login')
@user_required
def towing_edit(request, towing_id):
    """Edit an existing towing request"""
    towing = get_object_or_404(TowingRequest, pk=towing_id)
    
    # Only allow editing if not completed or cancelled
    if towing.status in ['completed', 'cancelled']:
        
        return redirect('towing_detail', towing_id=towing.id)
    
    if request.method == 'POST':
        form = TowingRequestForm(request.POST, instance=towing)
        if form.is_valid():
            form.save()
           
            return redirect('towing_detail', towing_id=towing.id)
    else:
        form = TowingRequestForm(instance=towing)
    
    return render(request, 'portal/towing_form.html', {'form': form, 'towing': towing, 'title': 'Edit Towing Request'})

@login_required(login_url='login')
@user_required
def towing_delete(request, towing_id):
    """Delete/Cancel a towing request"""
    towing = get_object_or_404(TowingRequest, pk=towing_id)
    
    if request.method == 'POST':
        towing.status = 'cancelled'
        towing.save()
        
        return redirect('dashboard')
    
    return render(request, 'portal/confirm_delete.html', {'object': towing, 'type': 'Towing Request'})

# ============ OTP VERIFICATION ============
@login_required(login_url='login')
@user_required
def verify_otp(request, booking_id):
    """Verify OTP for service booking completion"""
    booking = get_object_or_404(ServiceBooking, pk=booking_id)
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp == booking.otp:
            booking.otp_verified = True
            booking.status = 'completed'
            booking.save()
            
            return redirect('booking_detail', booking_id=booking.id)
    return render(request, 'portal/verify_otp.html', {'booking': booking})

@login_required(login_url='login')
@user_required
def verify_towing_otp(request, towing_id):
    """Verify OTP for towing request completion"""
    towing = get_object_or_404(TowingRequest, pk=towing_id)
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        if entered_otp == towing.otp:
            towing.otp_verified = True
            towing.status = 'completed'
            towing.save()
            
            return redirect('towing_detail', towing_id=towing.id)
        
           
    return render(request, 'portal/verify_towing_otp.html', {'towing': towing})

