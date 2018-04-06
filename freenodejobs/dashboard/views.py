from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from freenodejobs.utils.paginator import AutoPaginator


@login_required
def view(request):
    jobs = request.user.jobs.all()

    page = AutoPaginator(request, jobs, 20).current_page()

    return render(request, 'dashboard/view.html', {
        'page': page,
    })
