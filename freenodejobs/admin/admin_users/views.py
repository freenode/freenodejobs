from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST

from freenodejobs.utils.paginator import AutoPaginator
from freenodejobs.utils.decorators import staff_required

from .forms import FilterForm, UserForm

User = get_user_model()


@staff_required
def view(request):
    form = FilterForm(request.GET)

    if not form.is_valid():
        return HttpResponseBadRequest(form.errors.as_json())

    qs = User.objects.all()
    page = AutoPaginator(request, form.apply_filter(qs), 20).current_page()

    return render(request, 'admin/users/view.html', {
        'form': form,
        'page': page,
    })


@staff_required
def edit(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)

        if form.is_valid():
            form.save()

            messages.success(request, "User updated.")

            return redirect(request.path)
    else:
        form = UserForm(instance=user)

    return render(request, 'admin/users/edit.html', {
        'form': form,
        'user': user,
    })


@require_POST
@staff_required
def admin_toggle(request, user_id, enable):
    user = get_object_or_404(User, pk=user_id)
    user.is_staff = enable
    user.save()

    msg = "User with email {} has been configured as an admin." \
        if enable else "Admin privileges for {} have been removed."
    messages.success(request, msg.format(user.email))

    return redirect('admin:users:view')
