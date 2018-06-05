from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout

from freenodejobs.utils.user import login
from freenodejobs.utils.tokens import get_user_from_token
from freenodejobs.utils.decorators import logout_required

from .forms import RegistrationForm


@logout_required
def view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('registration:success')

    else:
        form = RegistrationForm()

    return render(request, 'registration/view.html', {
        'form': form,
    })


@logout_required
def success(request):
    return render(request, 'registration/success.html')


def validate(request, token):
    # Always log the user out, at least to avoid confusion
    logout(request)

    user = get_user_from_token(token)

    if user is None or user.email_validated:
        messages.error(request,
                       "The link you followed is invalid or has expired.")
        return redirect(settings.LOGOUT_REDIRECT_URL)

    user.email_validated = timezone.now()
    user.save()

    login(request, user)

    messages.success(request, "Email successfully validated.")

    return redirect(settings.LOGIN_REDIRECT_URL)
