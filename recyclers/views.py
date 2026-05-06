from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Avg, Q
from households.models import WastePickupRequest
from core.models import WasteCategory, EducationalContent
from .models import RecyclerProfile, Review, RecyclerNotification
from datetime import datetime, timedelta

@login_required
def recycler_dashboard(request):
    if request.user.role != 'recycler':
        return redirect('households:dashboard')
    
    try:
        profile = request.user.recycler_profile
    except RecyclerProfile.DoesNotExist:
        profile = RecyclerProfile.objects.create(user=request.user)
    
    if not profile.is_approved:
        return render(request, 'recyclers/pending_approval.html')
    
    # Stats
    completed_count = WastePickupRequest.objects.filter(
        recycler=request.user,
        status='completed'
    ).count()
    
    pending_count = WastePickupRequest.objects.filter(
        recycler=request.user,
        status='accepted'
    ).count()
    
    avg_rating = Review.objects.filter(recycler=request.user).aggregate(Avg('rating'))['rating__avg'] or 0
    
    unread_notifications = RecyclerNotification.objects.filter(
        recycler=request.user,
        is_read=False
    ).count()
    
    # Recent pickups
    recent_pickups = WastePickupRequest.objects.filter(
        recycler=request.user
    ).order_by('-created_at')[:5]
    
    context = {
        'profile': profile,
        'completed_count': completed_count,
        'pending_count': pending_count,
        'avg_rating': round(avg_rating, 1),
        'unread_notifications': unread_notifications,
        'recent_pickups': recent_pickups,
    }
    return render(request, 'recyclers/dashboard.html', context)

@login_required
def pickup_requests(request):
    """All available pickup requests with filters"""
    if request.user.role != 'recycler':
        return redirect('home')
    
    requests = WastePickupRequest.objects.filter(
        status='pending',
        pickup_date__gte=datetime.now().date()
    )
    
    # Filters
    category = request.GET.get('category')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    area = request.GET.get('area')
    
    if category:
        requests = requests.filter(waste_category_id=category)
    if date_from:
        requests = requests.filter(pickup_date__gte=date_from)
    if date_to:
        requests = requests.filter(pickup_date__lte=date_to)
    if area:
        requests = requests.filter(Q(address__icontains=area) | Q(household__city__icontains=area))
    
    requests = requests.order_by('pickup_date', 'pickup_time')
    waste_categories = WasteCategory.objects.all()
    
    context = {
        'requests': requests,
        'waste_categories': waste_categories,
        'selected_category': category,
        'date_from': date_from,
        'date_to': date_to,
        'area': area,
    }
    return render(request, 'recyclers/pickup_requests.html', context)

@login_required
def pickup_detail(request, pk):
    """Detailed view of a pickup request before accepting"""
    if request.user.role != 'recycler':
        return redirect('home')
    
    pickup = get_object_or_404(WastePickupRequest, pk=pk)
    
    context = {
        'pickup': pickup,
    }
    return render(request, 'recyclers/pickup_detail.html', context)

@login_required
def accept_pickup(request, pk):
    if request.user.role != 'recycler':
        messages.error(request, 'Access denied')
        return redirect('home')
    
    pickup = get_object_or_404(WastePickupRequest, pk=pk, status='pending')
    pickup.recycler = request.user
    pickup.status = 'accepted'
    pickup.save()
    
    messages.success(request, 'Pickup request accepted!')
    return redirect('recyclers:pickup_requests')

@login_required
def complete_pickup(request, pk):
    if request.user.role != 'recycler':
        messages.error(request, 'Access denied')
        return redirect('home')
    
    pickup = get_object_or_404(WastePickupRequest, pk=pk, recycler=request.user, status='accepted')
    pickup.status = 'completed'
    pickup.save()
    
    # Create notification for review
    RecyclerNotification.objects.create(
        recycler=request.user,
        notification_type='review_received',
        title='Pickup Completed',
        message=f'Pickup for {pickup.household.name} has been completed. Waiting for review.',
        pickup_request=pickup
    )
    
    messages.success(request, 'Pickup marked as completed!')
    return redirect('recyclers:dashboard')

@login_required
def pickup_history(request):
    """Completed pickups history with filters"""
    if request.user.role != 'recycler':
        return redirect('home')
    
    pickups = WastePickupRequest.objects.filter(
        recycler=request.user
    ).exclude(status='pending')
    
    # Filters
    category = request.GET.get('category')
    status = request.GET.get('status')
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if category:
        pickups = pickups.filter(waste_category_id=category)
    if status:
        pickups = pickups.filter(status=status)
    if date_from:
        pickups = pickups.filter(pickup_date__gte=date_from)
    if date_to:
        pickups = pickups.filter(pickup_date__lte=date_to)
    
    pickups = pickups.order_by('-pickup_date', '-pickup_time')
    waste_categories = WasteCategory.objects.all()
    
    context = {
        'pickups': pickups,
        'waste_categories': waste_categories,
        'selected_category': category,
        'selected_status': status,
        'date_from': date_from,
        'date_to': date_to,
    }
    return render(request, 'recyclers/pickup_history.html', context)

@login_required
def notifications(request):
    """Notifications page for recyclers"""
    if request.user.role != 'recycler':
        return redirect('home')
    
    notifications = RecyclerNotification.objects.filter(recycler=request.user)
    
    # Mark as read if requested
    if request.GET.get('mark_read'):
        notification_id = request.GET.get('mark_read')
        RecyclerNotification.objects.filter(id=notification_id, recycler=request.user).update(is_read=True)
        return redirect('recyclers:notifications')
    
    context = {
        'notifications': notifications,
    }
    return render(request, 'recyclers/notifications.html', context)

@login_required
def reviews(request):
    """Reviews page for recyclers"""
    if request.user.role != 'recycler':
        return redirect('home')
    
    reviews = Review.objects.filter(recycler=request.user)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    total_reviews = reviews.count()
    
    # Rating distribution
    rating_dist = {}
    for i in range(1, 6):
        rating_dist[i] = reviews.filter(rating=i).count()
    
    context = {
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1),
        'total_reviews': total_reviews,
        'rating_dist': rating_dist,
    }
    return render(request, 'recyclers/reviews.html', context)

@login_required
def earnings_stats(request):
    """Earnings and stats page"""
    if request.user.role != 'recycler':
        return redirect('home')
    
    profile = request.user.recycler_profile
    
    # Stats
    total_completed = WastePickupRequest.objects.filter(
        recycler=request.user,
        status='completed'
    ).count()
    
    # This month
    this_month = WastePickupRequest.objects.filter(
        recycler=request.user,
        status='completed',
        pickup_date__month=datetime.now().month,
        pickup_date__year=datetime.now().year
    ).count()
    
    # By category
    by_category = WastePickupRequest.objects.filter(
        recycler=request.user,
        status='completed'
    ).values('waste_category__name').annotate(count=Count('id')).order_by('-count')
    
    # Recent activity
    recent_activity = WastePickupRequest.objects.filter(
        recycler=request.user,
        status='completed'
    ).order_by('-pickup_date')[:10]
    
    context = {
        'profile': profile,
        'total_completed': total_completed,
        'this_month': this_month,
        'by_category': by_category,
        'recent_activity': recent_activity,
    }
    return render(request, 'recyclers/earnings_stats.html', context)

@login_required
def recycling_guidelines(request):
    """Recycling guidelines for recyclers"""
    if request.user.role != 'recycler':
        return redirect('home')
    
    waste_categories = WasteCategory.objects.all()
    educational_content = EducationalContent.objects.filter(
        is_published=True,
        content_type__in=['guide', 'article']
    )
    
    context = {
        'waste_categories': waste_categories,
        'educational_content': educational_content,
    }
    return render(request, 'recyclers/recycling_guidelines.html', context)

@login_required
def edit_profile(request):
    if request.user.role != 'recycler':
        messages.error(request, 'Access denied')
        return redirect('home')
    
    try:
        profile = request.user.recycler_profile
    except RecyclerProfile.DoesNotExist:
        profile = RecyclerProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        profile.bio = request.POST.get('bio')
        profile.service_areas = request.POST.get('service_areas')
        profile.vehicle_type = request.POST.get('vehicle_type')
        profile.is_available = request.POST.get('is_available') == 'on'
        profile.save()
        
        request.user.phone = request.POST.get('phone')
        request.user.address = request.POST.get('address')
        request.user.city = request.POST.get('city')
        request.user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('recyclers:dashboard')
    
    return render(request, 'recyclers/edit_profile.html', {'profile': profile})
