from django.shortcuts import render


def landing(request):
    return render(request, 'static/landing.html')


def privacy_policy(request):
    return render(request, 'static/privacy_policy.html')


def terms_of_service(request):
    return render(request, 'static/terms_of_service.html')
