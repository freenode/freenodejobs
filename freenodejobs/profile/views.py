from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .forms import ProfileForm


@login_required
def view(request):
    profile = getattr(request.user, 'profile', None)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            profile, created = form.save(request.user)

            if created:
                messages.success(request,
                                 "Profile created! You can now create jobs.")
                return redirect('jobs:add-edit:add')

            messages.success(request, "Profile saved.")

            return redirect(request.path)
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'profile/view.html', {
        'form': form,
        'profile': profile,
    })
