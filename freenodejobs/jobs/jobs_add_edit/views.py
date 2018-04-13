from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from freenodejobs.utils.decorators import ajax

from ..enums import StateEnum

from .forms import AddEditForm, RemoveForm, SubmitForApprovalForm, AddTagForm


@login_required
def view(request, slug=None):
    job = None

    if slug is not None:
        job = get_object_or_404(request.user.jobs.editable(), slug=slug)

    if not hasattr(request.user, 'profile'):
        return redirect('profile:view')

    if request.method == 'POST':
        form = AddEditForm(request.POST, instance=job)

        if form.is_valid():
            job = form.save(request.user)

            return redirect(job)

    else:
        form = AddEditForm(instance=job)

    return render(request, 'jobs/add_edit/view.html', {
        'job': job,
        'form': form,
        'state_enum': list(StateEnum),
    })


@login_required
def remove(request, slug):
    job = get_object_or_404(request.user.jobs.editable(), slug=slug)

    if request.method == 'POST':
        form = RemoveForm(job, request.POST)
        if form.is_valid():
            form.save(request.user)
            messages.success(request, "Your job was removed.")

            return redirect('dashboard:view')
    else:
        form = RemoveForm(job)

    return render(request, 'jobs/add_edit/remove.html', {
        'job': job,
        'form': form,
    })


@require_POST
@login_required
def submit_for_approval(request, slug):
    job = get_object_or_404(request.user.jobs.editable(), slug=slug)

    form = SubmitForApprovalForm(job, request.POST)
    if form.is_valid():
        form.save(request.user)

    messages.success(request, "Your job has been submitted for approval.")

    return redirect('dashboard:view')


@ajax()
@require_POST
@login_required
def xhr_add_tag(request):
    form = AddTagForm(request.POST)

    if not form.is_valid():
        return HttpResponseBadRequest()

    tag = form.save(request.user)

    return render(request, 'jobs/add_edit/xhr_add_tag.html', {
        'tag': tag,
    })
