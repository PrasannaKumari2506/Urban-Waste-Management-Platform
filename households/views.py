from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import WastePickupRequest
from core.models import WasteCategory, EducationalContent
from recyclers.models import Review
from accounts.models import User
from datetime import datetime

@login_required
def dashboard(request):
    if request.user.role != 'household':
        return redirect('recyclers:dashboard')
    
    waste_categories = WasteCategory.objects.all()
    pending_pickups = WastePickupRequest.objects.filter(
        household=request.user,
        status='pending'
    ).count()
    
    upcoming_pickups = WastePickupRequest.objects.filter(
        household=request.user,
        status='accepted',
        pickup_date__gte=datetime.now().date()
    ).order_by('pickup_date', 'pickup_time')[:5]
    
    recent_educational = EducationalContent.objects.filter(is_published=True)[:3]
    
    nearby_recyclers = User.objects.filter(
        role='recycler',
        recycler_profile__is_approved=True,
        recycler_profile__is_available=True
    ).annotate(
        total_pickups=Count('assigned_pickups', filter=Q(assigned_pickups__status='completed'))
    )[:5]
    
    context = {
        'waste_categories': waste_categories,
        'pending_pickups': pending_pickups,
        'upcoming_pickups': upcoming_pickups,
        'educational_content': recent_educational,
        'nearby_recyclers': nearby_recyclers,
    }
    return render(request, 'households/dashboard.html', context)

@login_required
def request_pickup(request):
    if request.user.role != 'household':
        messages.error(request, 'Access denied')
        return redirect('home')
    
    if request.method == 'POST':
        waste_category_id = request.POST.get('waste_category')
        description = request.POST.get('description')
        pickup_date = request.POST.get('pickup_date')
        pickup_time = request.POST.get('pickup_time')
        address = request.POST.get('address')
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        
        try:
            waste_category = WasteCategory.objects.get(id=waste_category_id)
            WastePickupRequest.objects.create(
                household=request.user,
                waste_category=waste_category,
                description=description,
                pickup_date=pickup_date,
                pickup_time=pickup_time,
                address=address or request.user.address,
                latitude=latitude or request.user.latitude,
                longitude=longitude or request.user.longitude
            )
            messages.success(request, 'Pickup request submitted successfully!')
            return redirect('households:dashboard')
        except Exception as e:
            messages.error(request, f'Error creating request: {str(e)}')
    
    waste_categories = WasteCategory.objects.all()
    return render(request, 'households/request_pickup.html', {'waste_categories': waste_categories})

@login_required
def pickup_history(request):
    if request.user.role != 'household':
        messages.error(request, 'Access denied')
        return redirect('home')
    
    pickups = WastePickupRequest.objects.filter(household=request.user).order_by('-created_at')
    return render(request, 'households/pickup_history.html', {'pickups': pickups})

@login_required
def add_review(request, pk):
    if request.user.role != 'household':
        messages.error(request, 'Access denied')
        return redirect('home')
    
    pickup = get_object_or_404(WastePickupRequest, pk=pk, household=request.user, status='completed')
    
    if hasattr(pickup, 'review'):
        messages.warning(request, 'You have already reviewed this pickup')
        return redirect('households:pickup_history')
    
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment')
        
        Review.objects.create(
            recycler=pickup.recycler,
            household=request.user,
            pickup_request=pickup,
            rating=rating,
            comment=comment
        )
        messages.success(request, 'Review submitted successfully!')
        return redirect('households:pickup_history')
    
    return render(request, 'households/add_review.html', {'pickup': pickup})

@login_required
def educational_content(request):
    content = EducationalContent.objects.filter(is_published=True)
    content_type = request.GET.get('type')
    if content_type:
        content = content.filter(content_type=content_type)
    return render(request, 'households/educational_content.html', {'content': content})
