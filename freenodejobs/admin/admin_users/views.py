from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST

from freenodejobs.utils.paginator import AutoPaginator
from freenodejobs.utils.decorators import staff_required

User = get_user_model()


@staff_required
def view(request):
    users = User.objects.order_by('-is_staff', 'date_joined')

    page = AutoPaginator(request, users, 20).current_page()

    return render(request, 'admin/users/view.html', {
        'page': page,
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
