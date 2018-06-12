from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from freenodejobs.jobs.enums import StateEnum
from freenodejobs.utils.paginator import AutoPaginator
from freenodejobs.utils.decorators import staff_required

from freenodejobs.jobs.models import Job

from .forms import ApproveForm, RejectForm, RemoveForm


@staff_required
def view(request, state_slug=''):
    try:
        state = StateEnum[state_slug.upper()]
    except KeyError:
        return redirect(
            'admin:view',
            StateEnum.WAITING_FOR_APPROVAL.name.lower(),
        )

    jobs = Job.objects.filter(state=state)
    page = AutoPaginator(request, jobs, 20).current_page()

    by_state = Job.objects.by_state()

    return render(request, 'admin/view.html', {
        'page': page,
        'state': state,
        'by_state': by_state,
    })


@staff_required
def approve(request, slug):
    job = get_object_or_404(Job, slug=slug)

    if request.method == 'POST':
        form = ApproveForm(job, request.POST)
        if form.is_valid():
            form.save(request.user)
            messages.success(request, "Job was approved.")

            return redirect('admin:view')
    else:
        form = ApproveForm(job)

    return render(request, 'admin/approve.html', {
        'job': job,
        'form': form,
    })


@staff_required
def reject(request, slug):
    job = get_object_or_404(Job, slug=slug)

    if request.method == 'POST':
        form = RejectForm(job, request.POST)
        if form.is_valid():
            form.save(request.user)
            messages.success(request, "Job was rejected.")

            return redirect('admin:view')
    else:
        form = RejectForm(job)

    return render(request, 'admin/reject.html', {
        'job': job,
        'form': form,
    })


@staff_required
def remove(request, slug):
    job = get_object_or_404(Job, slug=slug)

    if request.method == 'POST':
        form = RemoveForm(job, request.POST)
        if form.is_valid():
            form.save(request.user)
            messages.success(request, "Job was removed.")

            return redirect('admin:view')
    else:
        form = RemoveForm(job)

    return render(request, 'admin/remove.html', {
        'job': job,
        'form': form,
    })
