from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect

from freenodejobs.utils.user import login
from freenodejobs.utils.decorators import logout_required

from .forms import RegistrationForm


@logout_required
def view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registered.")

            return redirect(settings.LOGIN_REDIRECT_URL)

    else:
        form = RegistrationForm()

    return render(request, 'registration/view.html', {
        'form': form,
    })
