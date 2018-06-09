from django.conf import settings
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

from freenodejobs.utils.user import login
from freenodejobs.utils.tokens import get_user_from_token, get_value_from_token

from .forms import ChangeEmailForm


@login_required
def view(request):
    if request.method == 'POST':
        form = ChangeEmailForm(request.POST, instance=request.user)

        if form.is_valid():
            email = form.save()

            messages.success(
                request,
                "A validation email has been sent to {}.".format(email)
            )

            return redirect('profile:view')

    else:
        form = ChangeEmailForm(instance=request.user)

    return render(request, 'account/change_email/view.html', {
        'form': form,
    })


def validate(request, token):
    # Always log the user out, at least to avoid confusion
    logout(request)

    user = get_user_from_token(token)
    new_email = get_value_from_token(token, 0)

    if user is None or new_email is None:
        messages.error(request,
                       "The link you followed is invalid or has expired.")
        return redirect(settings.LOGOUT_REDIRECT_URL)

    user.email = new_email
    user.email_validated = timezone.now()
    user.save()

    login(request, user)

    messages.success(
        request,
        "Your new email address was successfully validated.",
    )

    return redirect(settings.LOGIN_REDIRECT_URL)
