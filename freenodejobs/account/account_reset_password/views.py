from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model

from freenodejobs.utils.user import login
from freenodejobs.utils.decorators import logout_required

from .forms import EmailForm, SetPasswordForm
from .utils import get_user_from_token


UserModel = get_user_model()


@logout_required
def view(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request,
                             "Instructions to reset your password have been "
                             "sent to the specified address if it exists.")
            return redirect(request.path)

    else:
        form = EmailForm()

    return render(request, 'account/reset_password/view.html', {
        'form': form,
    })


@logout_required
def reset(request, token):
    user = get_user_from_token(token)

    if user is None:
        messages.error(request,
                       "The link you followed is invalid or has expired.")
        return redirect(settings.LOGIN_REDIRECT_URL)

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)

        if form.is_valid():
            form.save()
            login(request, user)
            messages.success(request, "Your password has been set.")

            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = SetPasswordForm(user)

    return render(request, 'account/reset_password/reset.html', {
        'form': form,
    })
