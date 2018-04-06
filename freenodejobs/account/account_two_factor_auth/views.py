from two_factor import views as two_factor_views
from two_factor.utils import default_device, devices_for_user
from two_factor.views.utils import class_view_decorator

from django.contrib import messages
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required


@login_required
def view(request):
    return render(request, 'account/two_factor_auth/view.html', {
        'default_device': default_device(request.user),
    })


@login_required
def enabled(request):
    messages.success(request, "Two factor authentication enabled.")

    return redirect('account:two-factor-auth:view')


@require_POST
@login_required
def disable(request):
    for x in devices_for_user(request.user):
        x.delete()

    messages.success(request, "Two factor authentication disabled.")

    return redirect('account:two-factor-auth:view')


@class_view_decorator(login_required)
class SetupView(two_factor_views.SetupView):
    qrcode_url = 'account:two-factor-auth:qr-code'
    success_url = 'account:two-factor-auth:enabled'
    template_name = 'account/two_factor_auth/setup.html'


@class_view_decorator(login_required)
class QRGeneratorView(two_factor_views.QRGeneratorView):
    pass
