from django.shortcuts import render
from django.contrib import messages
from .ml_classifier import classifier


def home(request):
    if request.user.is_authenticated:
        if request.user.role == 'household':
            return render(request, 'households/dashboard.html')
        elif request.user.role == 'recycler':
            return render(request, 'recyclers/dashboard.html')
    return render(request, 'core/home.html')


def waste_classifier(request):
    """Waste classifier page with image upload."""
    return render(request, 'core/waste_classifier.html')


def classify_image(request):
    """Process uploaded image and return classification result."""
    if request.method != 'POST' or not request.FILES.get('waste_image'):
        messages.error(request, 'Please upload an image.')
        return render(request, 'core/waste_classifier.html')

    image_file = request.FILES['waste_image']

    # Validate file type
    allowed_types = {'image/jpeg', 'image/jpg', 'image/png', 'image/webp'}
    if image_file.content_type not in allowed_types:
        messages.error(
            request,
            'Please upload a valid image file (JPG, PNG, or WEBP).'
        )
        return render(request, 'core/waste_classifier.html')

    # Validate file size (max 10 MB)
    if image_file.size > 10 * 1024 * 1024:
        messages.error(request, 'Image must be smaller than 10 MB.')
        return render(request, 'core/waste_classifier.html')

    try:
        result = classifier.classify_waste(image_file)

        if result.get('error'):
            messages.error(request, f"Classification failed: {result['message']}")
            return render(request, 'core/waste_classifier.html')

        return render(request, 'core/waste_classifier.html', {'result': result})

    except Exception as exc:
        messages.error(request, f'Unexpected error: {exc}')
        return render(request, 'core/waste_classifier.html')
