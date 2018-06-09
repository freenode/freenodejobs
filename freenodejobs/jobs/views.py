from django.shortcuts import render, get_object_or_404, redirect, Http404

from freenodejobs.utils.paginator import AutoPaginator

from .forms import FilterForm
from .enums import StateEnum
from .models import Job


def view(request, job_type=None):
    form = FilterForm(job_type, request.GET)

    # Redirect if we need to
    target = form.get_redirect()
    if target:
        return redirect(target)

    qs = form.get_queryset()

    page = AutoPaginator(request, qs, 20).current_page()

    return render(request, 'jobs/view.html', {
        'page': page,
        'form': form,
    })


def job(request, slug, prefix=None):
    job = get_object_or_404(Job, slug=slug)

    # Removed jobs are not visible by anyone
    if job.state == StateEnum.REMOVED:
        return render(request, 'jobs/removed.html', status=410)

    def can_view():
        # Live jobs are always viewable
        if job.state == StateEnum.LIVE:
            return True

        # You can always view your "own" jobs
        if request.user == job.user:
            return True

        # Staff members can view any job
        if request.user.is_staff:
            return True

        return False

    if not can_view():
        raise Http404()

    if request.path != job.get_absolute_url():
        return redirect(job.get_absolute_url())

    return render(request, 'jobs/job.html', {
        'job': job,
    })
